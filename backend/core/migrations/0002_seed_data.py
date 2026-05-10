from django.db import migrations


def seed_data(apps, schema_editor):
    Category = apps.get_model("core", "Category")
    Course = apps.get_model("core", "Course")

    cats = {
        "Web Development": Category.objects.create(name="Web Development", icon="🌐"),
        "Data Science": Category.objects.create(name="Data Science", icon="📊"),
        "Design": Category.objects.create(name="Design", icon="🎨"),
        "Mobile Dev": Category.objects.create(name="Mobile Dev", icon="📱"),
        "Cybersecurity": Category.objects.create(name="Cybersecurity", icon="🔒"),
        "AI & ML": Category.objects.create(name="AI & ML", icon="🤖"),
    }

    courses = [
        {
            "title": "Full-Stack Web Development Bootcamp",
            "description": "Master HTML, CSS, JavaScript, React, Node.js, and databases. Build 10 real-world projects and land your first developer job.",
            "instructor": "Dr. Angela Yu",
            "category": cats["Web Development"],
            "level": "beginner",
            "duration_hours": 65,
            "rating": 4.8,
            "students_enrolled": 18420,
            "price": 1299.00,
            "is_featured": True,
        },
        {
            "title": "Python for Data Science & Machine Learning",
            "description": "Learn Python, NumPy, Pandas, Matplotlib, Scikit-Learn, and TensorFlow. Real datasets, real projects.",
            "instructor": "Jose Portilla",
            "category": cats["Data Science"],
            "level": "intermediate",
            "duration_hours": 42,
            "rating": 4.7,
            "students_enrolled": 12800,
            "price": 999.00,
            "is_featured": True,
        },
        {
            "title": "UI/UX Design Mastery with Figma",
            "description": "Go from zero to hero in UI/UX design. Learn Figma, design thinking, user research, and prototyping.",
            "instructor": "Daniel Scott",
            "category": cats["Design"],
            "level": "beginner",
            "duration_hours": 28,
            "rating": 4.9,
            "students_enrolled": 9320,
            "price": 799.00,
            "is_featured": True,
        },
        {
            "title": "React Native — Build iOS & Android Apps",
            "description": "Build cross-platform mobile apps with React Native. Push notifications, maps, and camera integration included.",
            "instructor": "Stephen Grider",
            "category": cats["Mobile Dev"],
            "level": "intermediate",
            "duration_hours": 38,
            "rating": 4.6,
            "students_enrolled": 7540,
            "price": 899.00,
            "is_featured": False,
        },
        {
            "title": "Ethical Hacking & Penetration Testing",
            "description": "Learn offensive security, network scanning, exploitation, and writing professional pentest reports.",
            "instructor": "Zaid Sabih",
            "category": cats["Cybersecurity"],
            "level": "advanced",
            "duration_hours": 50,
            "rating": 4.7,
            "students_enrolled": 6120,
            "price": 1099.00,
            "is_featured": False,
        },
        {
            "title": "Deep Learning & Neural Networks with PyTorch",
            "description": "Build CNNs, RNNs, Transformers, and GANs from scratch. Train on GPUs and deploy to production.",
            "instructor": "Andrew Ng",
            "category": cats["AI & ML"],
            "level": "advanced",
            "duration_hours": 55,
            "rating": 4.9,
            "students_enrolled": 14200,
            "price": 1499.00,
            "is_featured": True,
        },
        {
            "title": "Django REST Framework — Build Production APIs",
            "description": "Learn Django, DRF, JWT auth, PostgreSQL, Docker, and deploy to cloud. Build a full SaaS backend.",
            "instructor": "Mosh Hamedani",
            "category": cats["Web Development"],
            "level": "intermediate",
            "duration_hours": 30,
            "rating": 4.8,
            "students_enrolled": 5480,
            "price": 799.00,
            "is_featured": False,
        },
        {
            "title": "Data Visualization with D3.js",
            "description": "Create stunning interactive charts, dashboards, and maps using D3.js, SVG, and modern JavaScript.",
            "instructor": "Curran Kelleher",
            "category": cats["Data Science"],
            "level": "intermediate",
            "duration_hours": 20,
            "rating": 4.5,
            "students_enrolled": 3200,
            "price": 599.00,
            "is_featured": False,
        },
    ]

    for c in courses:
        Course.objects.create(**c)


def unseed_data(apps, schema_editor):
    Category = apps.get_model("core", "Category")
    Course = apps.get_model("core", "Course")
    Course.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
