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
    clinics = Clinic.objects.all()

    if location:
        clinics = clinics.filter(location=location)

    clinic_data = []
    for clinic in clinics:
        clinic_data.append({
            "name": clinic.name,
            "address": clinic.address,
            "location": clinic.location,
            "image_url": clinic.image.url if clinic.image else '',  # Ensure that we include the image URL
        })

    return JsonResponse({'clinics': clinic_data})


from .models import Clinic

import requests
from django.http import JsonResponse
from django.conf import settings

from django.http import JsonResponse
import requests
from django.conf import settings

def nearby_clinics(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not lat or not lng:
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

    # Google Maps Places API endpoint for finding nearby clinics
    places_url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}"
        "&radius=5000"  # Search within 5 km
        "&type=veterinary_care"  # Type of place
        f"&key={settings.GOOGLE_MAPS_API_KEY}"
    )

    response = requests.get(places_url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch places from Google Maps API'}, status=response.status_code)

    data = response.json()

    # Extract relevant clinic information
    clinics = []
    for place in data.get("results", []):
        place_name = place.get("name")
        vicinity = place.get("vicinity")
        place_id = place.get("place_id")

        # Attempt to retrieve the photo reference for images
        photo_reference = None
        photos = place.get("photos", [])
        if photos:
            photo_reference = photos[0].get("photo_reference")

        # Construct the image URL from the photo reference if available
        if photo_reference:
            image_url = (
                f"https://maps.googleapis.com/maps/api/place/photo"
                f"?maxwidth=400"
                f"&photoreference={photo_reference}"
                f"&key={settings.GOOGLE_MAPS_API_KEY}"
            )
        else:
            image_url = "https://via.placeholder.com/400"  # Default placeholder

        # Append clinic data
        clinics.append({
            "name": place_name,
            "address": vicinity,
            "location": "Nearby",
            "image_url": image_url,
        })

    return JsonResponse({'clinics': clinics})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings

def send_adoption_email(request):
    if request.method == 'POST':
        # Get form data (you may want to validate these)
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')

        # Compose the email content
        subject = 'Adoption Form Submission'
        message = f"Thank you for submitting the adoption form, {first_name} {last_name}.\n\n" \
                  "Please visit the location for further instructions."

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # You need to configure this in settings.py
            [email],  # Send to the user's email address
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
