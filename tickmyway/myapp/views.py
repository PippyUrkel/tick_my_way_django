from django.shortcuts import render, redirect
from django.urls import reverse
from .models import get_login_dates, find_user, generate_and_store_content, get_generated_items
from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import jwt
from django.conf import settings
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from docx import Document
import mimetypes

# MongoDB connection details
uri = 'mongodb+srv://andre:WangoTango238@tick-my-way.fiy3g.mongodb.net/?retryWrites=true&w=majority&appName=tick-my-way'  # Replace with your actual MongoDB URI


client = MongoClient(uri, server_api=ServerApi('1'))
db = client['SITE_DETAILS']
users_collection = db['Users']
lookup_collection = db['Institute_Lookup']
subjects_collection = db['Subjects']
map_collection = db['Paths']



# JWT Authentication Decorator
def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            return redirect('login')
        
        try:
            # Verify token and decode payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Add email to request for view functions to use
            request.user_email = payload['email']
        except jwt.ExpiredSignatureError:
            return redirect('login')
        except jwt.InvalidTokenError:
            return redirect('login')
            
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def landing_page(request):
    return render(request, 'landing-page/landing.html', {})

def profile(request):
    email = "andredsouza256@gmail.com"  # Replace with dynamic email from session or request
    user = find_user(email)  # Assuming you have a function to find the user by email
    login_dates = get_login_dates(email)
    print(login_dates)
    
    context = {
        'login_dates': login_dates,
        'name': user['name'],
        'email': user['email']
    }
    
    return render(request, 'streak-info/streak-info.html', context)

def skill_page(request):
    return render(request, 'roadmap-render/skill-page.html', {})

def skill_selection(request):
    if request.method == 'POST':
        selected_skills = request.POST.get('selected_skills', '')
        selected_skills_list = selected_skills.split(',')
        # Process the selected skills as needed
        # For example, save them to the user's profile or session
        request.session['selected_skills'] = selected_skills_list
        return redirect(reverse('onboarding_quiz'))  # Redirect to the next step
    return render(request, 'roadmap-render/skill-page.html')

def onboarding_quiz(request):
    selected_skills = request.session.get('selected_skills', [])
    # Render the quiz page with the selected skills
    return render(request, 'roadmap-render/onboarding-quiz.html', {'selected_skills': selected_skills})

def dashboard(request):
    return render(request, 'student-dashboard-new/studentdashboard.html', {})

@jwt_required
def student_dashboard(request):
    user = request.user

    # For now, simulate user information
    user_email = "demo_user@example.com"  # Replace this with a mock or default value
    user_institute = "Demo University"
    user_experience = 5
    user_platinum = True
    user_level = 3

    # Simulate fetching data
    subjects_list = [
        {"title": "Math 101", "description": "Basic Mathematics", "instructor": "Dr. Smith"},
        {"title": "History 202", "description": "World History", "instructor": "Prof. Jones"},
    ]
    mentors_list = ["Dr. Smith", "Prof. Jones"]
    student_count = 50
    mentor_count = 10
    current_strength = mentor_count + student_count

    return render(
        request,
        "student-dashboard-new/studentdashboard.html",
        {
            "subjects": subjects_list,
            "mentors": mentors_list,
            "experience": user_experience,
            "platinum": user_platinum,
            "level": user_level,
            "student_count": student_count,
            "mentor_count": mentor_count,
            "institute_name": user_institute,
            "current_strength": current_strength,
        },
    )

@jwt_required
def student_shop(request):
    return render(request, "student-dashboard-new/student-shop.html")

@jwt_required
def student_profile(request):
    return render(request, "student-dashboard-new/student-profile.html", {"count": 4})

@jwt_required
def student_courses(request):
    user = request.user_email
    student = users_collection.find_one({"email": user})
    student_email = student['email']
    student_university = student['institute']

    course_title = request.GET.get('title')
    mentor_name = request.GET.get('mentor')

    subjects = list(subjects_collection.find({"enrolled_students.student_email": student_email}))
    course_list = []
    class_comments = []

    for subject in subjects:
        mentor = users_collection.find_one({"email": subject["instrcutor_email"]})
        if mentor and mentor['institute'] == student_university:
            course_list.append({
                "title": subject["title"],
                "description": subject.get("description", ""),
                "instructor": mentor["username"]
            })
            if subject["title"] == course_title:
                class_comments = subject.get("class_comments", [])

    class_comments.sort(key=lambda x: x["timestamp"], reverse=True)
    return render(request, "student-dashboard-new/student-courses.html", {
        "course_list": course_list,
        "course_name": course_title,
        "mentor_name": mentor_name,
        "class_comments": class_comments
    })
@csrf_exempt
@jwt_required
def upload_file(request):
    if request.method == 'POST':
        try:
            if 'file' not in request.FILES:
                messages.error(request, 'No file uploaded')
                return redirect('roadmap')
            
            file = request.FILES['file']
            if not file.name.endswith('.docx'):
                messages.error(request, 'Only .docx files allowed')
                return redirect('roadmap')
            
            # Save and process file
            file_path = default_storage.save(f'uploads/{file.name}', file)
            doc = Document(default_storage.path(file_path))
            
            # Extract content
            content = []
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    content.append(paragraph.text)
                    
            # Store in session
            request.session['file_content'] = '\n'.join(content)
            request.session['filename'] = file.name
            
            # Cleanup
            default_storage.delete(file_path)
            
            return redirect('roadmap')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('roadmap')
    
    return redirect('roadmap')

@jwt_required
def roadmap(request):
    # Get email from JWT token
    user_email = request.user_email
    
    # Get generated items for roadmap
    items = get_generated_items(user_email, q_topic="python")
    
    # Build context with both items and file data
    context = {
        'items': items,
        'file_content': request.session.get('file_content'),
        'filename': request.session.get('filename')
    }
    
    return render(request, 'roadmap-render/roadmap.html', context)