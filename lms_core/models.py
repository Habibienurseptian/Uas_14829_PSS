from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

# Category model
class Category(models.Model):
    name = models.CharField("Category Name", max_length=200)
    description = models.TextField("Category Description", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="Teacher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Course model
class Course(models.Model):
    name = models.CharField("Nama Course", max_length=200)
    description = models.TextField("Description", null=True, blank=True)
    price = models.IntegerField("Harga")
    image = models.ImageField("Banner", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="Pengajar", on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Add max_students to limit course enrollment
    max_students = models.PositiveIntegerField("Max Students", default=30)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Daftar Course"

    def __str__(self) -> str:
        return self.name + " : " + str(self.price)

    def get_member_count(self):
        """Returns the number of members enrolled in the course."""
        return CourseMember.objects.filter(course_id=self).count()

    def is_full(self):
        """Checks if the course has reached the maximum number of students."""
        return self.get_member_count() >= self.max_students


ROLE_OPTIONS = [('std', "Siswa"), ('ast', "Asisten")]

# Course Member model
class CourseMember(models.Model):
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, verbose_name="siswa", on_delete=models.RESTRICT)
    roles = models.CharField("peran", max_length=3, choices=ROLE_OPTIONS, default='std')
    is_completed = models.BooleanField("Completed", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"

    def __str__(self) -> str:
        return f"{self.course_id} : {self.user_id}"

    @classmethod
    def bulk_enroll(cls, course, student_users):
        enrollments = []
        for student in student_users:
            enrollments.append(cls(course_id=course, user_id=student))

        try:
            cls.objects.bulk_create(enrollments)
        except IntegrityError:
            pass
    def save(self, *args, **kwargs):
        if CourseMember.objects.filter(course_id=self.course_id, user_id=self.user_id).exists():
            raise IntegrityError("Student is already enrolled in this course.")
        super().save(*args, **kwargs)


# Course Content model
class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField('URL Video', max_length=200, null=True, blank=True)
    file_attachment = models.FileField("File", null=True, blank=True)
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    parent_id = models.ForeignKey("self", verbose_name="induk", on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"

    def __str__(self) -> str:
        return f'[{self.course_id}] {self.name}'


# Comment model with moderation
class Comment(models.Model):
    content_id = models.ForeignKey(CourseContent, verbose_name="konten", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="pengguna", on_delete=models.CASCADE)
    comment = models.TextField('komentar')
    is_approved = models.BooleanField("Approved for Display", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"

    def __str__(self) -> str:
        return f"Komen: {self.content_id.name} - {self.user_id}"

    @classmethod
    def approved_comments(cls):
        """Return only approved comments."""
        return cls.objects.filter(is_approved=True)

class CompletionTracking(models.Model):
    student = models.ForeignKey(User, verbose_name="Siswa", on_delete=models.CASCADE)
    course_content = models.ForeignKey(CourseContent, verbose_name="Konten Matkul", on_delete=models.CASCADE)
    completed_at = models.DateTimeField("Tanggal Penyelesaian", auto_now_add=True)

    class Meta:
        verbose_name = "Completion Tracking"
        verbose_name_plural = "Completion Trackings"
        unique_together = ['student', 'course_content']  # Ensure one student cannot complete the same content twice

    def __str__(self) -> str:
        return f"{self.student} - {self.course_content.name}"
