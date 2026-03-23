from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import OTP
import random
from  django.http import HttpResponse

# Create your views here.
@login_required
def home(request):
   
    return render(request,'home.html')
def resume_analyzer(request):
    return render(request,'resume_analyzer.html')

#login
def login_(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid username and password')  
            return redirect('login_')          
    return render(request,'login_.html')


def logout_(request):
    logout(request)
    return redirect('login_')

#register 
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
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
        if not request.user.is_authenticated:
            return redirect('login_')
        U=request.user
        U.first_name=request.POST.get('fname','')
        U.last_name=request.POST.get('lname' ,'')
        U.email=request.POST.get('email','')
        U.save()
        messages.success(request,'profile updated susccessfully !')
        return redirect('profile')    
    return render(request,'profile.html')
def contact(request):
    return render(request,'contact.html')    
def job_tracker(request):
    return render(request,'job_tracker.html')


#forget password logic with otp verification
def forget_pasw(request):
    

    if request.method=='POST':
     
        username=request.POST.get('uname','').strip()
        if not username:
            messages.error(request,"please enter your username")
            return render(request,'forget_pasw.html')
        try:
            u=User.objects.get(username=username)
            #genretate the 6 didgit otp from gmail 
            otp_code =str(random.randint(100000,999999))
            #otp save to database
            OTP.objects.create(user=u,otp_code=otp_code)
            #send otp to email
            try:
                send_mail(
                subject='your otp code -AI CAREER ASSISTANT',
                message=f'''
                hi {u.username},
                your otp is:{otp_code}
                this code expires in the 10 minutes.
                Do not share this code with anyone 
                -AI CAREER ASSITANT 
                ''',
                from_email=None,
                recipient_list=[u.email],
                fail_silently=False )
              
                #save userame in the session 
                request.session['fp_user']=u.username
                messages.success(request,f'otp sent your email')
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request,f'email sending failed:{str(e)}') 
                return render(request,'forget_pasw.html')  
        except User.DoesNotExist:
            messages.error(request,'username not found')   
    return render(request,'forget_pasw.html')

#vedrify otp
def verify_otp(request):
    username=request.session.get('fp_user')
    if not username:
        return redirect('forget_pasw')
    if request.method=='POST':
        entered_otp=request.POST['otp']
        try:
            user=User.objects.get(username=username)
            #get the latetest unused otp
            otp_obj=OTP.objects.filter(
                user=user,
                otp_code=entered_otp,
                is_used=False
            ).latest( 'created_at')
            #check if the expired
            if otp_obj.is_expired():
                messages.error(request,'OTP has expired. please try again.')
                return render(request,'verify_otp.html')
            #mark as otp
            otp_obj.is_used=True
            otp_obj.save()
            #allow password reset
            request.session['otp_verified']=True
            return redirect('new_pasw')
        except OTP.DoesNotExist:
            messages.error(request,"invalid otp.please try again")
        
    return render(request,'verify_otp.html')
#new password
def new_pasw(request):
    username=request.session.get('fp_user')
    verified=request.session.get('otp_verified')
    if not username or not verified:
        return redirect('forget_pasw')
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExits:
        return redirect('forget_pasw')
    if request.method=='POST':
        new_password=request.POST['new_pasw']
        new_password2=request.POST['new_pasw2']
        if new_password!=new_password2:
            messages.error(request,'password do not match')
            return render(request,'new_pasw.html')
        if len(new_password)<6:
            messages.error(request,'password must be at least 6 charaters')
            return render(request,'new_pasw.html')
        
        user.set_password(new_password)
        user.save()
        #clear session
        del request.session['fp_user']
        del request.session['otp_verified']
        messages.success(request,'password changed! Please login.')
        return redirect('login_')
    

    return render(request,'new_pasw.html')

def test_email(request):
    return HttpResponse("working")