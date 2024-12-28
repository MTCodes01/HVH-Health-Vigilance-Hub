from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def home(request):
    # return render(request, 'index.html')
    return JsonResponse({"success": "success"}, status=200)