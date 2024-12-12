"""
URL configuration for tickmyway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import landing_page, profile, roadmap, skill_page, onboarding_quiz, dashboard, student_dashboard, student_courses, student_profile, student_shop, upload_file
from myapp.auth import login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('roadmap/', roadmap, name='roadmap'),
    path('skill-page/', skill_page, name='skill-page'),
    path('skill-page/onboarding-quiz', onboarding_quiz, name='onboarding-quiz'),
    path('dashboard', dashboard, name='dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('student-dashboard/shop/', student_shop, name='student_shop'),
    path('student-dashboard/student-profile/', student_profile, name='student_profile'),
    path('student-dashboard/courses/', student_courses, name='student_courses'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload-file/', upload_file, name='upload_file'),
]
