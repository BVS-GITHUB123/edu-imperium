from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="📚")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    duration_hours = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    students_enrolled = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    thumbnail_url = models.URLField(blank=True, default="")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Enrollment(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("email", "course")

    def __str__(self):
        return f"{self.name} → {self.course.title}"
