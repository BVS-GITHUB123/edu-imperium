from django.contrib import admin
from .models import Category, Course, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon"]
    search_fields = ["name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title", "instructor", "category", "level",
        "rating", "students_enrolled", "price", "is_featured",
    ]
    list_filter = ["level", "category", "is_featured"]
    search_fields = ["title", "instructor"]
    list_editable = ["is_featured", "rating"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "course", "enrolled_at"]
    list_filter = ["course"]
    search_fields = ["name", "email"]
    readonly_fields = ["enrolled_at"]
