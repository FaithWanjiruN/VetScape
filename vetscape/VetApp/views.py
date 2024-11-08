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
    return render(request, 'home.html') 

@login_required(login_url='login')
def home(request):
    return render (request,'home.html')


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
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def  logout(request):
    return redirect('home')