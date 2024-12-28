from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def heatmap(request):
    return render(request, 'heatmap.html')

def forgot(request):
    return render(request, 'forgot.html')