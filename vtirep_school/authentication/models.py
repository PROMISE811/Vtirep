from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('staff', 'Staff'), ('admin', 'Admin')])
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course_choices = [
        ('family_therapy', 'Family Therapy'),
        ('nursing', 'Nursing'),
        ('social_work', 'Social Work'),
    ]
    course = models.CharField(max_length=50, choices=course_choices)

    def __str__(self):
        return f"{self.user.username} - {self.get_course_display()}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)  # Example additional field

    # Fixing the conflict with related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customUser_set',  # You can change this to another name if you prefer
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customUser_set',  # Again, change the name if needed
        blank=True
    )

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)  # A, B, C, etc.

    def __str__(self):
        return f'{self.student.username} - {self.assignment.title}: {self.grade}'
