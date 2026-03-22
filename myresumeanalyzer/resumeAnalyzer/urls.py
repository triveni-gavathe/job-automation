from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('resume_analyzer/',resume_analyzer,name='resume_analyzer'),
    path('login_/',login_ ,name='login_'),
    path('register/',register ,name='register'),
    path('profile/',profile ,name='profile'),
    path('logout_/', logout_,name='logout_'),
    path('contact/',contact,name='contact'),
    path('job_tracker/',job_tracker,name='job_tracker'),
    path('forget_pasw/',forget_pasw,name='forget_pasw'),
    
]