# FILE: myapp/forms.py
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

class SignupForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

class AddCourseForm(forms.Form):
    course_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}))
    course_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Description'}))
    max_students = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Students'}))
