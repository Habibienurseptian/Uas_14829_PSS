from django.contrib import admin
from lms_core.models import Course
from .models import Category

# Customize Course model in the Django admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "teacher", "category", "max_students", "created_at"]
    list_filter = ["teacher", "category"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fields = ["name", "description", "price", "image", "teacher", "category", "max_students", "created_at", "updated_at"]

# Customize Category model in the Django admin (Optional)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "teacher", "created_at", "updated_at"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    fields = ["name", "description", "teacher", "created_at", "updated_at"]

