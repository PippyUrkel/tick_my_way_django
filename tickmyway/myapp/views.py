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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import JsonResponse
from .forms import AddCourseForm
from django.core.files.storage import default_storage



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

def roadmap(request):
    user_email = "andredsouza256@gmail.com"  # Replace with dynamic email from session or request
    items = get_generated_items(user_email, q_topic="Arts Craft")
    return render(request, 'roadmap-render/roadmap.html', {'items': items})

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

def student_dashboard(request):
    token = request.COOKIES.get('access_token')

    if not token:
        return JsonResponse({'error': 'Token is missing'}, status=401)

    try:
        # Decode the token to get the payload
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_email = decoded_token.get('email')
        
        if not user_email:
            return JsonResponse({'error': 'Email not found in token'}, status=401)
        
        print(f"dashboard : {user_email}")

        # Fetch user information
        user_info = users_collection.find_one({"email": user_email})
        user_lastactive = user_info['login_dates'][-1]
        user_experience = user_info['experience']
        user_platinum = user_info['platinum']
        user_level = user_info['level']

        # Fetch subjects where the user_email is mentioned in enrolled_students
        subjects = subjects_collection.find({"enrolled_students.student_email": user_email})
        subjects_list = []
        mentors_set = set()

        for subject in subjects:
            # Check the mentor's university
            mentor = users_collection.find_one({"email": subject["instrcutor_email"]})
            if mentor:
                subjects_list.append({
                    "title": subject["title"],
                    "description": subject.get("description", ""),
                    "instructor": mentor["username"]  # Fetch the mentor's name
                })
                # Collect mentor's name
                mentors_set.add(mentor["username"])
        
        mentors_list = list(mentors_set)

        # Calculate streak
        streak = len(user_lastactive)
        user_streak = streak
        print(subjects_list)
        print(mentors_list)

        return render(request, 'student-dashboard-new/studentdashboard.html', {
            'user_email': user_email,
            'user_lastactive': user_lastactive,
            'user_streak': user_streak,
            'user_experience': user_experience,
            'user_platinum': user_platinum,
            'user_level': user_level,
            'subjects_list': subjects_list,
            'mentors_list': mentors_list,
        })
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)

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

def roadmap(request):
    user_email = "andredsouza256@gmail.com"
    items = get_generated_items(user_email, q_topic="Arts Craft")
    
    context = {
        'items': items,
        'file_content': request.session.get('file_content'),
        'filename': request.session.get('filename')
    }
    return render(request, 'roadmap-render/roadmap.html', context)


def greeting(request):
    return render(request, 'landing-page/greeeting.html', {})

"""THIS IS THE INSTRUCTOR SIDE THIS IS THE INSTRUCTOR SIDE THIS IS THE INSTRUCTOR SIDE"""

def instructor_home(request):
    user = "jose10sojan@gmail.com"
    role = users_collection.find_one({"email": user}).get("role")
    if role != "mentor":
        return redirect("access_denied")

    instructor_name = users_collection.find_one({"email": user}).get("username")
    instructor_inst = users_collection.find_one({"email": user}).get("institute")

    subjects = subjects_collection.find({"instructor_email": user})
    subjects_list = [
        {
            "title": subject["title"],
            "enrolled_students": subject["enrolled_students"],
        }
        for subject in subjects
    ]

    return render(
        request,
        "instructor-dashboard/home.html",
        {
            "instructor_name": instructor_name,
            "instructor_inst": instructor_inst,
            "identity": user,
            "subjects": subjects_list,
        },
    )

from django.contrib.auth.models import AnonymousUser



def instructor_course(request):
    user = "jose10sojan@gmail.com"
    role = users_collection.find_one({"email": user}).get("role")


    form = AddCourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_course = {
            "title": form.cleaned_data["course_name"],
            "description": form.cleaned_data["course_description"],
            "instrcutor_email": user,
            "max_students": form.cleaned_data["max_students"],
            "enrolled_students": [],
        }
        subjects_collection.insert_one(new_course)
        messages.success(request, "New course added successfully!")
        return redirect("instructor_course")

    subjects = subjects_collection.find({"instrcutor_email": user})
    subjects_list = [
        {
            "title": subject["title"],
            "description": subject.get("description", ""),
            "enrolled_students": subject["enrolled_students"],
        }
        for subject in subjects
    ]
    return render(request, "instructor-dashboard/courses.html", {"form": form, "subjects": subjects_list})


def instructor_course_forwarded(request, name):
    user = "jose10sojan@gmail.com"

    subject_title = name.replace("-", " ")
    subject = subjects_collection.find_one({"title": subject_title, "instrcutor_email": user})


    return render(request, "instructor-dashboard/viewcourse.html", {"subject": subject})

def instructor_grading(request):
    user = "jose10sojan@gmail.com"
    role = users_collection.find_one({"email": user})['role']
    subjects = subjects_collection.find({"instrcutor_email": user})
    students_list = []
    for subject in subjects:
        for student in subject["enrolled_students"]:
            students_list.append({
                "name": student["student_email"],
                "status": student["status"],
                "subject": subject["title"]
            })
    
    return render(request, "instructor-dashboard/grading.html", {"students": students_list})

def instructor_grading_forwarded(request):
    student_name = request.GET.get('student')
    subject_name = request.GET.get('subject')
    
    user = "jose10sojan@gmail.com"
    role = users_collection.find_one({"email": user.email})['role']

    subject = subjects_collection.find_one({"title": subject_name, "instrcutor_email": user.email})
    if not subject:
        return redirect('access_denied')
    
    student_data = next((student for student in subject["enrolled_students"] if student["student_email"] == student_name), None)
    if not student_data:
        return redirect('access_denied')
    
    return render(request, "instructor-dashboard/gradingforward.html", {
        "student_name": student_name,
        "subject_name": subject_name,
        "student_data": student_data
    })


def access_denied(request):
    return render(request, "instructor-dashboard/denied.html")

def instructor_reminders(request):
    return render(request, 'instructor-dashboard/reminders.html')


@csrf_exempt
def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        if document.name.endswith('.docx'):
            filename = "jose10sojan@gmail.com-resource.docx"
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
            default_storage.save(file_path, document)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return JsonResponse({'error': 'Invalid file type. Only .docx files are allowed.'}, status=400)
    return JsonResponse({'error': 'No file uploaded'}, status=400)