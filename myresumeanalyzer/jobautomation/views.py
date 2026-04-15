from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import job,Application,jobAlert
from .scraper import search_jobs
from django.contrib import messages


# Create your views here.
def job_home(request):
    application=Application.objects.filter(
        user=request.user
    ).order_by('-applied_date')
    stats={
        'total':application.count(),
        'applied':application.filter(status='applied').count(),
        'interviewe':application.filter(status='interview').count(),
        'rejected':application.filter(status='rejected').count(),
        'offer':application.filter(status='offer').count(),
        
            
    }
    return render(request,'job_tracker.html',{
        'applications':application,
        'stats':stats
        
        
    })
    
#-----job serach -----
@login_required
def job_search(request):
    jobs=[]
    role=''
    location=''    
    if request.method=='POST':
        role=request.POST.get('role','').strip()
        location=request.Post.get('location','').strip()
        if role and location:
            jobs=search_jobs(role,location)
            if not jobs:
                messages.info(request,"no jobs found .try diffrent keywords")
        else:
            messages.error(request,'please enter role and location')        
    return render(request,'job_search.html',{
        'jobs':jobs,
        'role':role,
        'location':location
        
    })
#save job
