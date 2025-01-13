from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course
from .models import StudentProfile
from .models import Assignment, Resource

class CustomUserCreationForm(UserCreationForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        empty_label="Select a course",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'course']


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    course = forms.ChoiceField(choices=StudentProfile.course_choices, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file']


