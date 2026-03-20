from django.shortcuts import render

# Create your views here.
def job_home(request):
    return render(request,'job_home.html')