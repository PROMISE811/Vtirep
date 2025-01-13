from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # If your authentication is in a separate app
    path('', views.home, name='home'),  # Add a view for the root URL
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    # Include any other URLs for your project
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
