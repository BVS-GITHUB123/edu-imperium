import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("icon", models.CharField(default="📚", max_length=50)),
            ],
            options={"verbose_name_plural": "categories"},
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("instructor", models.CharField(max_length=100)),
                ("level", models.CharField(choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")], default="beginner", max_length=20)),
                ("duration_hours", models.PositiveIntegerField(default=0)),
                ("rating", models.DecimalField(decimal_places=1, default=4.5, max_digits=3)),
                ("students_enrolled", models.PositiveIntegerField(default=0)),
                ("price", models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ("thumbnail_url", models.URLField(blank=True, default="")),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="courses", to="core.category")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField()),
                ("enrolled_at", models.DateTimeField(auto_now_add=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="core.course")),
            ],
            options={"unique_together": {("email", "course")}},
        ),
    ]
