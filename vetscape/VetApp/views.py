from django.shortcuts import render
from multiprocessing import Value
from .models import *
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime
from django.contrib import messages

def home(request):
    return render(request, 'index.html') 

@login_required(login_url='login')
def home(request):
    return render (request,'index.html')


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            # Create User object
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            
            # Create Customer object
            customer = customer(user=my_user)
            customer.save()
            
            return redirect('login')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def  logout(request):
    return redirect('index')


from django.conf import settings

api_key = settings.GOOGLE_MAPS_API_KEY

# views.py
from django.shortcuts import render

from django.http import JsonResponse
from .models import Clinic

def clinic_list(request):
    location = request.GET.get('location')
    clinics = Clinic.objects.filter(location=location) if location else Clinic.objects.all()

    clinic_data = [
        {
            "name": clinic.name,
            "address": clinic.address,
        }
        for clinic in clinics
    ]
    return JsonResponse({'clinics': clinic_data})


import requests
from django.http import JsonResponse
from django.conf import settings
from .models import Clinic

def nearby_clinics(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    places_url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}"
        "&radius=5000"
        "&type=veterinary_care"
        f"&key={settings.GOOGLE_MAPS_API_KEY}"
    )

    response = requests.get(places_url)
    data = response.json()

    clinics = [
        {
            "name": place.get("name"),
            "address": place.get("vicinity"),
        }
        for place in data.get("results", [])
    ]

    return JsonResponse({'clinics': clinics})

