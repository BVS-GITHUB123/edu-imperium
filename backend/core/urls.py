from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats),
    path("categories/", views.CategoryListView.as_view()),
    path("courses/", views.CourseListView.as_view()),
    path("courses/<int:pk>/", views.CourseDetailView.as_view()),
    path("enroll/", views.EnrollView.as_view()),
]
