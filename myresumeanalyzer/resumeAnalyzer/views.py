from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request,'home.html')
def resume_analyzer(request):
    return render(request,'resume_analyzer.html')