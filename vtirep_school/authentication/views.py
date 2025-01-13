from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Course, Assignment, Resource, Grade
from .forms import AssignmentForm, ResourceForm
from django.contrib.auth import login, logout
from .models import StudentProfile, CustomUser  # Import CustomUser instead of User
from .models import Course, User, Resource
from django.core.files.storage import FileSystemStorage

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create CustomUser (use your custom user model)
            user = CustomUser.objects.create_user(  # Use CustomUser instead of User
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            # Assign course to StudentProfile
            course = form.cleaned_data['course']
            StudentProfile.objects.create(user=user, course=course)
            login(request, user)  # Log the user in after creating
            return redirect('dashboard')  # Redirect to the dashboard or home page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after logging in
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


# Home view (protected by login_required)
@login_required
def home_view(request):
    return render(request, 'dashboard.html')  # Render the dashboard for logged-in users

@login_required
def course_detail_view(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    resources = Resource.objects.filter(course=course)
    return render(request, 'course_detail.html', {'course': course, 'assignments': assignments, 'resources': resources})

# View for assignments (students can view/submit)
@login_required
def assignment_view(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        grade = Grade.objects.create(assignment=assignment, student=request.user, grade=request.POST['grade'])
        return redirect('course_detail', course_id=assignment.course.id)
    return render(request, 'assignment_detail.html', {'assignment': assignment})

# View for uploading resources (staff only)
@login_required
def upload_resource_view(request, course_id):
    if not request.user.is_staff:
        return redirect('course_list')

    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ResourceForm()

    return render(request, 'upload_resource.html', {'form': form, 'course': course})

# views.py

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Only staff can access this page

    staff_members = CustomUser.objects.filter(is_staff=True)
    return render(request, 'staff_dashboard.html', {'staff_members': staff_members})


def home(request):
    return render(request, 'home.html')  # Make sure 'home.html' exists

def student_dashboard(request):
    return render(request, 'student dashboard.html')  # Ensure this template exists


def admin_dashboard(request):
    # Get statistics
    courses_count = Course.objects.count()
    users_count = User.objects.count()
    resources_count = Resource.objects.count()

    return render(request, 'admin_dashboard.html', {
        'courses_count': courses_count,
        'users_count': users_count,
        'resources_count': resources_count,
    })

def manage_courses(request):
    # Your logic for managing courses goes here
    # For example, retrieving all courses from the database
    courses = Course.objects.all()  # Assuming you have a Course model
    return render(request, 'manage_course.html', {'courses': courses})


def manage_users(request):
    if request.method == 'POST':
        # Handle adding a new user (could add validation here)
        name = request.POST.get('name')
        role = request.POST.get('role')
        username = name.lower().replace(' ', '')  # Simple username creation logic
        user = User.objects.create_user(username=username, password='password')  # Replace with proper password handling
        user.first_name = name
        user.save()

        # You can also add additional fields or logic for different roles

        return redirect('manage_users')  # Redirect back to the users page

    # Get all users
    users = User.objects.all()  # Modify query to filter or paginate as necessary
    return render(request, 'manage_users.html', {'users': users})


def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_resource')  # Redirect after successful upload
    else:
        form = ResourceForm()

    # Get all resources from the database
    resources = Resource.objects.all()

    return render(request, 'upload_resource.html', {
        'form': form,
        'resources': resources
    })

def manage_resources(request):
    # Fetch all resources from the database
    resources = Resource.objects.all()

    # Check for any additional logic like resource deletion, updating, etc.
    # For example, handle deleting a resource
    if request.method == 'POST' and 'delete_resource' in request.POST:
        resource_id = request.POST.get('resource_id')
        resource = Resource.objects.get(id=resource_id)
        resource.delete()

    return render(request, 'manage_resources.html', {
        'resources': resources
    })