from django.http import JsonResponse
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Course, Enrollment
from .serializers import CategorySerializer, CourseSerializer, EnrollmentSerializer


def health(request):
    return JsonResponse({"status": "EDUIMPERIUM LIVE"})


@api_view(["GET"])
def stats(request):
    """Platform-level stats shown on the landing page."""
    return Response(
        {
            "total_courses": Course.objects.count(),
            "total_students": Enrollment.objects.values("email").distinct().count(),
            "total_categories": Category.objects.count(),
            "featured_count": Course.objects.filter(is_featured=True).count(),
        }
    )


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.select_related("category").all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "instructor", "description"]
    ordering_fields = ["rating", "students_enrolled", "created_at", "price"]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        level = self.request.query_params.get("level")
        featured = self.request.query_params.get("featured")
        if category:
            qs = qs.filter(category__id=category)
        if level:
            qs = qs.filter(level=level)
        if featured == "true":
            qs = qs.filter(is_featured=True)
        return qs


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.select_related("category").all()
    serializer_class = CourseSerializer


class EnrollView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        enrollment = serializer.save()
        # Increment enrolled count on the course
        course = enrollment.course
        course.students_enrolled += 1
        course.save(update_fields=["students_enrolled"])
