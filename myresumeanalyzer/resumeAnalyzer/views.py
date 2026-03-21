from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
        
    return redirect('login')
def resume_analyzer(request):
    return render(request,'resume_analyzer.html')

#login
def login_(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid username and password')            
    return render(request,'login_.html')


def logout_(request):
    logout(request)
    return redirect('login_')

#register 
def register(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method=='POST':
        username=request.POST['uname']
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        Email=request.POST['email']
        password=request.POST['pasw']
        password2=request.POST['pasw2']
        if password != password2:
            messages.error(request,'password do not match')
            return render(request,'register.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'username already taken') 
            return render(request,'register.html')   
        
        else:
            U=User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=Email
            )
            U.set_password(password)
            U.save()
            login(request,U)
            messages.success(request,"account created successfully!")
            return redirect('home')               
    return render(request,'register.html')
@login_required
def profile(request):
    if request.method=='POST':
        U=request.user
        U.first_name=request.POST.get('first_name','')
        U.last_name=request.POST.get('last_name' ,'')
        U.email=request.POST.get('email','')
        U.save()
        messages.success(request,'profile updated susccessfully !')
        return redirect('profile')    
    return render(request,'profile.html')
def contact(request):
    return render(request,'contact.html')    
def job_tracker(request):
    return render(request,'job_tracker.html')
