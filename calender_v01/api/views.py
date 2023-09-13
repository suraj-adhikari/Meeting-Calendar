
from django.shortcuts import render
import requests
import threading
import json
from django.http import JsonResponse,HttpResponseRedirect
from django.http import HttpResponse
import time
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import userData,formData
from django.views.decorators.csrf import csrf_protect


# Our Hubspot url link to login through Hubspot
def hubspot_auth(request):
    # Construct the HubSpot OAuth2 authorization URL
    auth_url = f"https://app.hubspot.com/oauth/authorize?client_id={settings.HUBSPOT_CLIENT_ID}&scope=forms%20crm.objects.companies.write%20crm.objects.companies.read&redirect_uri={settings.HUBSPOT_REDIRECT_URI}"
    return HttpResponseRedirect(auth_url)

# Refresh token function to update access token after 30 min
def create_refresh_token():
    with open('access_token.json', 'r') as file:
        data = json.load(file)
    # Check if the required keys are present
    refresh_token = data.get('refresh_token', '')
    # Create the POST request data
    payload = {
        'grant_type': 'refresh_token',
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'client_secret': settings.HUBSPOT_CLIENT_SECRET,
        'redirect_uri': settings.HUBSPOT_REDIRECT_URI,
        'refresh_token': refresh_token
    }
    # Send the POST request
    token_url = 'https://api.hubapi.com/oauth/v1/token'
    response = requests.post(token_url, data=payload)
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        access_token = response.json().get('access_token')
        if 'access_token' in response_data:
            # Save the response data to the JSON file
            with open('access_token.json', 'w') as file:
                json.dump(response_data, file)
        
    return HttpResponse(access_token)

# Handle the OAuth2 callback and exchange the code for an access token
def hubspot_callback(request):
    code = request.GET.get('code')
    if code:
        token_url = 'https://api.hubapi.com/oauth/v1/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.HUBSPOT_CLIENT_ID,
            'client_secret': settings.HUBSPOT_CLIENT_SECRET,
            'redirect_uri': settings.HUBSPOT_REDIRECT_URI,
            'code': code,
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            with open('access_token.json', 'w') as token_file:
                json.dump(response.json(), token_file)
            # Schedule the creation of a refresh token after 28 minutes using threading
            time_to_wait = 1 * 60*28
            threading.Timer(time_to_wait, create_refresh_token).start()
            time_to_wait = 2 * 60*28
            threading.Timer(time_to_wait, create_refresh_token).start()
            time_to_wait = 3 * 60*28
            threading.Timer(time_to_wait, create_refresh_token).start()
            return HttpResponse(access_token)
    else:
        raise Exception("Hubspot is not sending code ")  
    return HttpResponse(access_token)



@csrf_protect
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            current_user=User.objects.create_user(uname,email,pass1)
            current_user.save()
            existing_data = userData.objects.filter(userName=uname, emailId=email)
            if existing_data.exists():
                print("You already have an account")
            else:
                wareHouse=userData(
                userName=uname,
                emailId=email,
                password1=pass1,
                password2=pass2,
            )
                wareHouse.save()
                # return redirect(f"https://app.hubspot.com/oauth/authorize?client_id={settings.HUBSPOT_CLIENT_ID}&scope=forms%20crm.objects.companies.write%20crm.objects.companies.read&redirect_uri={settings.HUBSPOT_REDIRECT_URI}")
                return redirect(f"https://app.hubspot.com/oauth/authorize?client_id={settings.HUBSPOT_CLIENT_ID}&scope=forms%20crm.objects.companies.write%20crm.objects.companies.read&redirect_uri={settings.HUBSPOT_REDIRECT_URI}")
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        current_username=request.POST.get('username')
        current_pass1=request.POST.get('pass')
        user=authenticate(request,username=current_username,password=current_pass1)
        if user is not None:
            login(request,user)
            return redirect(f"https://app.hubspot.com/oauth/authorize?client_id={settings.HUBSPOT_CLIENT_ID}&scope=forms%20crm.objects.companies.write%20crm.objects.companies.read&redirect_uri={settings.HUBSPOT_REDIRECT_URI}")
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
