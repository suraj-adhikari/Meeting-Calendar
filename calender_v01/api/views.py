
from django.shortcuts import render
import requests
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

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        apiKey=request.POST.get('apiKey')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            current_user=User.objects.create_user(uname,email,pass1)
            current_user.save()
            existing_data = userData.objects.filter(userName=uname, emailId=email,apiKey=apiKey)
            if existing_data.exists():
                print("You already have an account")
            else:
                wareHouse=userData(
                userName=uname,
                emailId=email,
                password1=pass1,
                password2=pass2,
                apiKey=apiKey
            )
                wareHouse.save()
                return redirect('home')
        

    return render (request,'signup.html')



def LoginPage(request):
    if request.method=='POST':
        current_username=request.POST.get('username')
        current_pass1=request.POST.get('pass')
        user=authenticate(request,username=current_username,password=current_pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')



def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def HomePage(request):
    try:
        # current user    
        current_user_email=request.user.email
        api_key=userData.objects.get(emailId=current_user_email).apiKey
        print(api_key)
        url="https://api.hubapi.com/marketing/v3/forms/"
        headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        data = response.json().get('results', [])
        for obj in data:
            id=obj['id']
            name=obj['name']
            createdAt=obj['createdAt']
            updatedAt=obj['updatedAt']
            apiKey=api_key
            existing_data = formData.objects.filter(formId=id)
            if existing_data.exists():
                print("form already added to  form data db")
            else:
                wareHouse=formData(
                formId=id,
                apiKey=apiKey,
                name=name,
                createdAt=createdAt,
                updatedAt=updatedAt)
                wareHouse.save()
    except :
        print("Error")
    total=formData.objects.all()
    if request.method=="POST":
        return redirect('user')
    return render (request,'home.html',{'total':total})



@login_required(login_url='login')
def user(request):
    # current user
        current_user_email=request.user.email
        api_key=userData.objects.get(emailId=current_user_email).apiKey
        print(api_key)
        url="https://api.hubapi.com/settings/v3/users/"
        headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        data = response.json().get('results', [])
        return render(request,'user.html',{'data':data})


# @login_required(login_url='login')
def calender(request):
    # we are using sleep or delay of 2 sec here  because form submission of data and fetch of data at same time cause error , so we check network it takes exact 1750ms to  do ,  so we make our fetch request 2 sec delay.
    # we can try reload functionality but it shows weird behaviour
    time.sleep(2)
    # API key
    api_key = 'pat-na1-8a689cf9-0e4f-4857-b529-e6ca79a230bd'
    
    # Make the API request
    url = 'https://api.hubapi.com/form-integrations/v1/submissions/forms/b0b4c739-3645-4a37-9c04-7f811d11ea4c'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json().get('results', [])
        # print(data) and optimize loop, you can check it using transeversing data
        user_data = [user['value'] for d in data for user in d.get('values', [])]
        # print(user_data)
        
        # Only take the first 5 elements of user_data
        user_data = user_data[:5]
        # print(user_data)
        
        country, requirement = user_data[3], user_data[4]

        print(country,requirement)
        vartika=['United States','Australia','Austria','Bolovia','Brazil','Canada','Chile','China','France','Germany','Hong Kong','Ireland','Iceland','Italy','United Kingdon']
        naman=['Zimbabwe','Zambia','Yemen','Vietnam','United Arab Emirates','Thailand','Sweden','Switzerland','Spain']
        hitesh=['Afghanistan','India','Pakistan','Bangladesh','Nepal','Bhutan','Sri Lanka','New Zealand','Myanmar','Malaysia','Maldives']
        aditya=['Poland','Portugal','Norway','Peru']

        print(country in vartika,country in naman,country in hitesh,country in aditya)
        if country in vartika and requirement == 'Others':
            print(f'Meeting assign to vartika from {country} and {requirement}')
            return HttpResponseRedirect('https://meetings.hubspot.com/vartika-khatri')
        elif  country in naman and requirement == 'Salesforce':
            print(f'Meeting assign to naman from {country} and {requirement}')
            return HttpResponseRedirect("https://meetings.hubspot.com/naman12")
        elif  country in hitesh and requirement == 'Hubspot':
            print(f'Meeting assign to hitesh from {country} and {requirement}')
            return HttpResponseRedirect("https://meetings.hubspot.com/hitesh19")
        elif country in aditya and requirement=='CMS':
            print(f'Meeting assign to aditya from {country} and {requirement}')
            return HttpResponseRedirect('https://meetings.hubspot.com/aditya-k1')
        else:
            print(f'Meeting assign to nanda from {country} and {requirement}')
            return HttpResponseRedirect('https://meetings.hubspot.com/nanda6')
            
        # return JsonResponse(user_data, safe=False)
    else:
        return JsonResponse({'message': 'Error occurred while fetching data'}, status=response.status_code)