# Import Section_______________________________________

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import User
from .models import PatientTicket
from folium.plugins import HeatMap
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import json
import pandas as pd
import requests
import csv
import joblib
import folium
import numpy as np

# API keys_____________________________________________

WEATHER_API_KEY = "3443df9e6a3d2df4ae5a38bca00b7619"

# API endpoints________________________________________

weather_base_url = "https://api.openweathermap.org/data/2.5/weather"

# Constants____________________________________________

SYMPTOM_DISEASE_MAP = {
    "fever": ["Dengue", "Malaria", "Flu", "Covid"],
    "cough": ["Covid", "Flu"],
    "rash": ["Dengue", "Measles"],
    "chills": ["Malaria"],
}

# Website Endpoints____________________________________

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

# def ticket(request):
#     return render(request, 'opTicket.html')

# Authentication_______________________________________

# @csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Data:",data)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            # first_name = data.get('firstName', '')
            # last_name = data.get('lastName', '')
            # age = data.get('age')
            # gender = data.get('gender')
            # current_address = data.get('currentAddress')
            # permanent_address = data.get('permanentAddress')
            # health_condition = data.get('healthCondition')
            # emergency_contact = data.get('emergencyContact')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists."}, status=400)

            # Create the user with the provided details
            user = User.objects.create_user(username=username, email=email, password=password)

            # Set additional fields specific to your custom User model
            # user.first_name = first_name
            # user.last_name = last_name
            # user.age = age
            # user.gender = gender
            # user.current_address = current_address
            # user.permanent_address = permanent_address
            # user.health_condition = health_condition
            # user.emergency_contact_name = emergency_contact.get("name")
            # user.emergency_contact_phone = emergency_contact.get("phone")
            # user.emergency_contact_relation = emergency_contact.get("relation")

            user.save()

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
            # Retrieve the user instance
            user = User.objects.get(username=username)

            # Update the User model with the provided data
            user.first_name = first_name
            user.last_name = last_name
            user.age = age
            user.gender = gender
            user.current_address = current_address
            user.permanent_address = permanent_address
            user.health_condition = health_condition
            user.emergency_contact_name = emergency_contact.get("name")
            user.emergency_contact_phone = emergency_contact.get("phone")
            user.emergency_contact_relation = emergency_contact.get("relation")
            user.save()
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        except Exception as e:
            print(f"Error saving query data: {e}")
            return JsonResponse({"error": "An error occurred while saving the query data."}, status=500)

        return JsonResponse({"success": "Query submitted successfully"}, status=200)

    return render(request, 'query.html')

def fetch_weather_data(lat, lon, api_key):
    url = f"{weather_base_url}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Latitude": lat,
            "Longitude": lon,
            "Temperature": data['main']['temp'],
            "Rainfall": data.get('rain', {}).get('1h', 0.0),
            "Humidity": data['main']['humidity'],
        }
    else:
        print(f"Error fetching weather data: {response.json()}")
        return None

from django.http import JsonResponse

def fetch_weather_for_location(request):
    if request.method == 'GET':
        try:
            lat = request.GET.get('lat')
            lon = request.GET.get('lon')

            if not lat or not lon:
                return JsonResponse({"error": "Latitude and longitude are required."}, status=400)

            # Fetch weather data
            weather_data = fetch_weather_data(lat, lon, WEATHER_API_KEY)

            if weather_data:
                return JsonResponse({"weather_data": weather_data}, status=200)
            else:
                return JsonResponse({"error": "Failed to fetch weather data."}, status=500)

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return JsonResponse({"error": "An internal server error occurred."}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use GET."}, status=405)

def predict_disease_view(data):
    try:
        symptoms = data.get('symptoms', [])
        lat = data.get('latitude')
        lon = data.get('longitude')
        estimated_days = data.get('estimated_days', 1)

        if not symptoms or not lat or not lon:
            return {"error": "Symptoms, latitude, and longitude are required."}

        # Fetch weather data
        weather_data = fetch_weather_data(lat, lon, WEATHER_API_KEY)
        if not weather_data:
            return {"error": "Failed to fetch weather data."}

        # Placeholder for density
        density = 5000  # Replace with actual logic or data

        # Predict disease
        predicted_disease = predict_disease_view({
            weather_data['Temperature'],
            weather_data['Humidity'],
            density,
            lat,
            lon,
            weather_data['Rainfall'],
            symptoms
        })

        # Generate heatmap
        location = [float(lat), float(lon)]
        heatmap_path = generate_heatmap(location, predicted_disease, estimated_days)

        return {
            "predicted_disease": predicted_disease,
            "heatmap_path": heatmap_path
        }

    except Exception as e:
        print(f"Error in disease prediction: {e}")
        return {"error": "An error occurred during disease prediction."}

def generate_heatmap(location, predicted_disease, estimated_days):
    m = folium.Map(location=location, zoom_start=10)
    for day in range(1, estimated_days + 1):
        radius = day * 10  # Increase radius per day
        HeatMap([[location[0], location[1], radius]]).add_to(m)

    # Create heatmap file path
    heatmap_file = f"heatmap_{predicted_disease}.html"
    heatmap_file_path = f"C:/Users/USER/OneDrive/Documents/vscode/HVH-Health-Vigilance-Hub/Backend/HVH/app/templates/{heatmap_file}"
    m.save(heatmap_file_path)
    
    print(f"Heatmap saved as {heatmap_file_path}")
    return heatmap_file_path

def train(request):
    weather_df = pd.read_csv("time_series_disease_data.csv")
    weather_df['Rainfall'] = weather_df.get('Rainfall', 0)

    X = weather_df[['Temperature', 'Humidity', 'Population Density', 'Latitude', 'Longitude', 'Rainfall']]
    y = weather_df['Disease']
    y = y.astype("category").cat.codes

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(model, "path/to/save/disease_predictor_model.pkl")
    print("\nModel saved successfully.")

# Ticket Data Handling__________________________________
# @csrf_exempt
# def ticket_handler(request):
#     if request.method == "POST":
#         try:
#             # Parse the incoming JSON data
#             data = json.loads(request.body)
            
#             # Convert date string to datetime object
#             dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            
#             # Create new ticket
#             ticket = PatientTicket.objects.create(
#                 firstName=data['firstName'],
#                 lastName=data['lastName'],
#                 dob=dob,
#                 gender=data['gender'],
#                 phone=data['phone'],
#                 email=data['email'],
#                 address=data['address']
#             )

#             # Predict the disease
#             symptoms = data.get('symptoms', [])
#             lat = data.get('latitude')
#             lon = data.get('longitude')
#             weather_data = fetch_weather_for_location(request)

#             if 'weather_data' not in weather_data:
#                 return JsonResponse({"error": "Failed to fetch weather data."}, status=500)
            
#             weather_data = weather_data['weather_data']
#             density = 5000  # Placeholder for density, replace with actual logic or data
            
#             predicted_disease = predict_disease(
#                 weather_data['Temperature'],
#                 weather_data['Humidity'],
#                 density,
#                 lat,
#                 lon,
#                 weather_data['Rainfall'],
#                 symptoms
#             )

#             # Generate heatmap
#             location = [float(lat), float(lon)]
#             generate_heatmap(location, predicted_disease, 1)

#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Ticket created and disease predicted successfully',
#                 'ticket_id': ticket.id,
#                 'predicted_disease': predicted_disease
#             })
            
#         except KeyError as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Missing required field: {str(e)}'
#             }, status=400)
            
#         except ValueError as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Invalid data format: {str(e)}'
#             }, status=400)
            
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Server error: {str(e)}'
#             }, status=500)
    
#     return render(request, 'opTicket.html')

@csrf_exempt
def ticket(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symptoms = data.get('symptoms', [])
            lat = data.get('latitude')
            lon = data.get('longitude')

            if not lat or not lon or not symptoms:
                return JsonResponse({
                    "status": "error",
                    "message": "Latitude, longitude, and symptoms are required."
                }, status=400)

            # Fetch weather data
            try:
                weather_data = fetch_weather_data(lat, lon, WEATHER_API_KEY)
                print(f"weather_response: {weather_data}")
                # weather_data = weather_response.get('weather_data', {})
                if not weather_data:
                    raise ValueError("Missing 'weather_data' in response.")
            except Exception as e:
                print(f"Error fetching weather data: {e}")
                return JsonResponse({
                    "status": "error",
                    "message": "Failed to fetch weather data."
                }, status=500)

            # Predict disease
            predicted_disease = predict_disease_view({
                weather_data['Temperature'],
                weather_data['Humidity'],
                5000,
                lat,
                lon,
                weather_data['Rainfall'],
                symptoms
            })

            # Generate heatmap
            location = [float(lat), float(lon)]
            heatmap_path = generate_heatmap(location, predicted_disease, 1)

            return JsonResponse({
                'status': 'success',
                'message': 'Disease predicted and heatmap generated successfully',
                'predicted_disease': predicted_disease,
                'heatmap': heatmap_path
            })
        except KeyError as e:
            return JsonResponse({
                "status": "error",
                "message": f"Missing key: {e}"
            }, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "status": "error",
                "message": "An error occurred during disease prediction."
            }, status=500)

    return render(request, 'opTicket.html')
