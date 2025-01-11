from django.shortcuts import render, redirect,  get_object_or_404, HttpResponse
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Course, CourseMember, Category, CompletionTracking, CourseContent
from django.views.decorators.http import require_POST


def index(request):
    return HttpResponse("<h1>Hello World</h1>")
    
def testing(request):
    dataCourse = Course.objects.all()
    dataCourse = serializers.serialize("python", dataCourse)
    return JsonResponse(dataCourse, safe=False)

def addData(request): # jangan lupa menambahkan fungsi ini di urls.py
    course = Course(
        name = "Belajar Django",
        description = "Belajar Django dengan Mudah",
        price = 1000000,
        teacher = User.objects.get(username="admin")
    )
    course.save()
    return JsonResponse({"message": "Data berhasil ditambahkan"})

def editData(request):
    course = Course.objects.filter(name="Belajar Django").first()
    course.name = "Belajar Django Setelah update"
    course.save()
    return JsonResponse({"message": "Data berhasil diubah"})

def deleteData(request):
    course = Course.objects.filter(name__icontains="Belajar Django").first()
    course.delete()
    return JsonResponse({"message": "Data berhasil dihapus"})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user object
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)  # Set password securely
            user.save()
            
            # Log the user in
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been registered successfully.')
                return redirect('login')  # Now points to the 'index' view
            else:
                messages.error(request, 'Authentication failed.')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('user_activity_dashboard')  # Redirect to the index page or home
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def some_protected_view(request):
    return render(request, 'protected.html')

@login_required
def user_activity_dashboard(request):
    user = request.user
    # Hitung jumlah kursus yang diikuti sebagai 'student'
    student_courses_count = CourseMember.objects.filter(user_id=user, roles='std').count()

    context = {
        'student_courses_count': student_courses_count,
    }
    return render(request, 'user_activity_dashboard.html', context)

def batch_enroll_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == "POST":
        # Assume we receive a list of usernames/emails
        student_usernames = request.POST.get("student_usernames").splitlines()  # Or however the list is provided
        
        student_users = []
        for username in student_usernames:
            try:
                user = User.objects.get(username=username)
                student_users.append(user)
            except User.DoesNotExist:
                messages.error(request, f"User with username {username} does not exist.")
        
        # Call the bulk_enroll method to enroll the students
        if student_users:
            CourseMember.bulk_enroll(course, student_users)
            messages.success(request, "Students have been successfully enrolled.")
        else:
            messages.error(request, "No valid students to enroll.")
    
    return render(request, "batch_enroll.html", {'course': course})

def course_analytics(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    member_count = course.get_member_count()  # Get the number of members for the course
    
    return render(request, "course_analytics.html", {
        "course": course,
        "member_count": member_count,
    })
    
@login_required
def certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the student is enrolled in the course
    try:
        course_member = CourseMember.objects.get(course_id=course, user_id=request.user)
    except CourseMember.DoesNotExist:
        raise Http404("You are not enrolled in this course.")

    # Check if the course is completed
    if not course_member.is_completed:
        return render(request, "course_not_completed.html")

    return render(request, "certificate.html", {
        "course": course_member.course_id,
        "student": course_member.user_id,
        "completion_date": course_member.updated_at,  # Date of completion
    })

    
@login_required
def add_category(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Or use the login URL for your application

    # Continue with category creation if user is logged in
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = Category.objects.create(
            name=name,
            description=description,
            teacher=request.user
        )
        return JsonResponse({"success": f"Category '{category.name}' added!"}, status=201)
    
    return render(request, "add_category.html")

@login_required
def show_categories(request):
    categories = Category.objects.filter(teacher=request.user)
    return render(request, "show_categories.html", {"categories": categories})

@login_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id, teacher=request.user)
        category.delete()
        return JsonResponse({"success": f"Category '{category.name}' deleted!"}, status=200)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found or you do not have permission to delete it."}, status=404)
    
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is full by comparing the number of enrolled students with the limit
    if course.get_member_count() >= course.max_students:
        messages.error(request, "This course has reached the maximum number of students.")
        return redirect('course_detail', course_id=course_id)

    # Enroll the student if not already enrolled
    if not CourseMember.objects.filter(course_id=course, user_id=request.user).exists():
        CourseMember.objects.create(course_id=course, user_id=request.user)
        messages.success(request, "You have successfully enrolled in the course.")
    else:
        messages.warning(request, "You are already enrolled in this course.")

    return redirect('course_detail', course_id=course_id)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})


@login_required
@require_POST
def add_completion(request, content_id):
    try:
        content = CourseContent.objects.get(id=content_id)
        # Ensure the student is enrolled in the course
        if not CourseMember.objects.filter(course_id=content.course_id, user_id=request.user).exists():
            return JsonResponse({"error": "You are not enrolled in this course."}, status=400)
        
        # Mark content as completed
        CompletionTracking.objects.create(student=request.user, course_content=content)
        return JsonResponse({"message": "Content marked as completed."}, status=200)
    
    except CourseContent.DoesNotExist:
        return JsonResponse({"error": "Content not found."}, status=404)
    
@login_required
def show_completion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Ensure the student is enrolled in the course
    if not CourseMember.objects.filter(course_id=course, user_id=request.user).exists():
        return JsonResponse({"error": "You are not enrolled in this course."}, status=400)

    completed_content = CompletionTracking.objects.filter(student=request.user, course_content__course_id=course)
    completed_content_list = [{"content_id": completion.course_content.id, "content_name": completion.course_content.name} for completion in completed_content]

    return JsonResponse({"completed_content": completed_content_list}, status=200)

@login_required
@require_POST
def delete_completion(request, content_id):
    try:
        content = CourseContent.objects.get(id=content_id)
        
        # Ensure the student has completed the content
        completion = CompletionTracking.objects.get(student=request.user, course_content=content)
        completion.delete()
        
        return JsonResponse({"message": "Completion status deleted."}, status=200)
    
    except CourseContent.DoesNotExist:
        return JsonResponse({"error": "Content not found."}, status=404)
    except CompletionTracking.DoesNotExist:
        return JsonResponse({"error": "Completion status not found."}, status=404)
