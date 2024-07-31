from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Profile
import random
import string

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def generate_password(request):
    if request.method == 'POST':
        length = int(request.POST.get('length', 8))
        option = request.POST.get('option', 'letters')
        
        if option == 'letters':
            characters = string.ascii_letters
        elif option == 'letters_numbers':
            characters = string.ascii_letters + string.digits
        elif option == 'letters_numbers_symbols':
            characters = string.ascii_letters + string.digits + string.punctuation
        else:
            characters = string.ascii_letters
        
        password = ''.join(random.choices(characters, k=length))
        profile = request.user.profile
        if profile.last_password == password:
            messages.error(request, 'New password cannot be the same as the last password')
            return redirect('generate_password')
        
        profile.last_password = password
        profile.save()
        messages.success(request, f'New password generated: {password}')
    
    return render(request, 'generate_password.html')

def user_logout(request):
    logout(request)
    return redirect('login')