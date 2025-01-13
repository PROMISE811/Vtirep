from django.contrib import admin
from .models import CustomUser, Course, StudentProfile
from django.contrib.auth.admin import UserAdmin
from .models import User, Resource, Assignment

# Register the Course model with its admin configuration
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)  # You can add description or any other relevant field

# Register the custom user model with UserAdmin for better customization
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'description')}),  # description field added
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'is_staff', 'description')  # Added description
    list_filter = ('is_staff', 'is_superuser', 'groups')  # Filters for admin view

# Register the StudentProfile model with its admin configuration
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')  # Displays user and course in the list view
    list_filter = ('course',)  # Filter by course
    search_fields = ('user__username', 'course')  # Enables search by username or course name
