from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from my_app.models import Person

# Create your views here.

def home_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request,'my_app/home.html')

def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request,'my_app/profile.html')

def login_page(request):
    
    if(request.method == 'POST'):
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            msg='Hello '+username+', You are successfully logged in'
            messages.success(request,msg)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")    
            return redirect('/login')
    
    return render(request,'my_app/login.html')

def signup_page(request):
    
    if(request.method == 'POST'):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        bio=request.POST['bio']
        gender=request.POST['gender']
        age=request.POST['age']
        
        if(int(age) <= 0):
            messages.info(request,'Invalid Age !')
            return redirect('/signup',name=username)
    
        if(User.objects.filter(username=username)):
            messages.info(request,username+' already exists !')
            return redirect('/signup')
        
        if(not username.isalnum()):
            messages.info(request,'Username must be Alpha-Numberic !')
            return redirect('/signup')
        
        if(User.objects.filter(email=email)):
            messages.info(request,email+' already exists !')
            return redirect('/signup')    
        
        myuser=User.objects.create_user(username,email,password)
        myuser.save()

        user=User.objects.get(username=myuser.username)
        person=Person.objects.create(added_by=user,name=username,bio=bio,age=age,gender=gender)
        person.save()
        
        print(person)
        messages.success(request,"Your Account has been successfully created")
        
        return redirect('/login')
    
    if request.user.is_authenticated:
        return redirect('/') 
       
    return render(request,'my_app/signup.html')


def log_out(request):
    logout(request)
    messages.success(request,"Succesfully logged out")
    
    return redirect('/login')