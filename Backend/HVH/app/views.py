# Import Section_______________________________________

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

# Endpoints____________________________________________

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

# def login(request):
#     return render(request, 'login.html')

# def signup(request):
#     return render(request, 'signup.html')

def heatmap(request):
    return render(request, 'heatmap.html')

def forgot(request):
    return render(request, 'forgot.html')

# def query(request):
#     return render(request, 'query.html')

def babyVaccination(request):
    return render(request, 'baby_vaccine.html')

def generalVaccination(request):
    return render(request, 'general_vaccine.html')

def profile(request):
    return render(request, 'profile.html')

def precaution(request):
    return render(request, 'precaution.html')

def virtualMeet(request):
    return render(request, 'virtual_meet.html')

def ticket(request):
    return render(request, 'opTicket.html')

# Authentication_______________________________________

# @csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists."}, status=400)

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create UserProfile instance if UserProfile table exists
            try:
                user_profile = UserProfile.objects.get_or_create(user=user)[0]
                user_profile.save()
            except Exception as profile_error:
                print(f"Error creating UserProfile: {profile_error}")

            return JsonResponse({"success": "User created successfully"}, status=201)

        except Exception as e:
            print(f"Error in signup view: {e}")
            return JsonResponse({"error": "An error occurred during sign-up."}, status=500)

    return render(request, 'signup.html')

# @csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({"success": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return render(request, 'login.html')

def query(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data.get('username')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        age = data.get('age')
        gender = data.get('gender')
        current_address = data.get('currentAddress')
        permanent_address = data.get('permanentAddress')
        health_condition = data.get('healthCondition')
        emergency_contact = data.get('emergencyContact')
        
        # Save the data to the database
        try:
            # Create a DataFrame from the data
            data = {
                "username": [username],
                "first_name": [first_name],
                "last_name": [last_name],
                "age": [age],
                "gender": [gender],
                "current_address": [current_address],
                "permanent_address": [permanent_address],
                "health_condition": [health_condition],
                "emergency_contact_name": [emergency_contact["name"]],
                "emergency_contact_phone": [emergency_contact["phone"]],
                "emergency_contact_relation": [emergency_contact["relation"]]
            }
            df = pd.DataFrame(data)

            # Save the DataFrame to user's profile
            try:
                user = User.objects.get(username=username)
                user_profile = UserProfile.objects.get(user=user)
                user_profile.data = df.to_csv(index=False)
                user_profile.save()
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)
        except Exception as e:
            print(f"Error saving query data: {e}")
            return JsonResponse({"error": "An error occurred while saving the query data."}, status=500)
        return JsonResponse({"success": "Query submitted successfully"}, status=200)
    return render(request, 'query.html')
  