from rest_framework import serializers
from .models import Category, Course, Enrollment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon"]


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "instructor",
            "category",
            "category_id",
            "level",
            "duration_hours",
            "rating",
            "students_enrolled",
            "price",
            "thumbnail_url",
            "is_featured",
            "created_at",
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "name", "email", "course", "course_title", "enrolled_at"]

    def validate(self, attrs):
        if Enrollment.objects.filter(
            email=attrs["email"], course=attrs["course"]
        ).exists():
            raise serializers.ValidationError(
                "You are already enrolled in this course."
            )
        return attrs
