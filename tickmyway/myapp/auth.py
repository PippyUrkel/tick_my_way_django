# FILE: myapp/views.py
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.contrib import messages
from datetime import datetime, timedelta
import jwt
from django.conf import settings


# MongoDB connection details
uri = 'mongodb+srv://andre:WangoTango238@tick-my-way.fiy3g.mongodb.net/?retryWrites=true&w=majority&appName=tick-my-way'  # Replace with your actual MongoDB URI

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['SITE_DETAILS']
users_collection = db['Users']
lookup_collection = db['Institute_Lookup']

def create_access_token(email):
    # Create payload
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=12),
        'iat': datetime.utcnow()
    }
    # Create token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        signup = SignupForm(request.POST)
        
        if 'email' in request.POST and 'password' in request.POST and 'confirm_password' not in request.POST:
            if form.is_valid():
                # Process the login form data
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                print(f"Login - Email: {email}, Password: {password}")
                
                # Check user in MongoDB
                check_user = users_collection.find_one({"email": email, "password": password})
                if check_user is None:
                    messages.error(request, 'Invalid email or password.')
                    return redirect('login')
                else:
                    # Create custom access token
                    access_token = create_access_token(email)
                    
                    messages.success(request, f'Login successful for {email}')
                    response = redirect('student_dashboard')
                    response.set_cookie(
                        'access_token',
                        access_token,
                        httponly=True,
                        max_age=3600 * 12  # 12 hours
                    )
                    return response

        elif 'email' in request.POST and 'password' in request.POST and 'confirm_password' in request.POST:
            if signup.is_valid():
                # Process the signup form data
                email = signup.cleaned_data['email']
                password = signup.cleaned_data['password']
                confirm_password = signup.cleaned_data['confirm_password']
                print(f"Signup - Email: {email}, Password: {password}, Confirm Password: {confirm_password}")
                
                # Check if user already exists
                check_user = lookup_collection.find_one({"email": email})
                if check_user is not None:
                    messages.error(request, 'User already exists.')
                    return redirect('login')
                else:
                    # Insert new user into MongoDB
                    new_user = {
                        "email": email,
                        "password": password
                    }
                    users_collection.insert_one(new_user)
                    messages.success(request, 'Signup successful. Please log in.')
                    return redirect('login')

    else:
        form = LoginForm()
        signup = SignupForm()

    return render(request, 'authentication/auth.html', {'form': form, 'signup': signup})

