from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'), #home page
    path('resume_analyzer/',resume_analyzer,name='resume_analyzer'), #resume analyzer page
    path('login_/',login_ ,name='login_'),#login page
    path('register/',register ,name='register'), #register page
    path('profile/',profile ,name='profile'), #profile page
    path('logout_/', logout_,name='logout_'), #logout page
    path('contact/',contact,name='contact'),  #contact page
    path('job_tracker/',job_tracker,name='job_tracker'), #job tracker page
    path('forget_pasw/',forget_pasw,name='forget_pasw'), #forget password page 
    path('verify_otp/',verify_otp,name='verify_otp'), #verify otp page
    path('new_pasw/',new_pasw,name='new_pasw'), #new password page
    path('test_email/',test_email,name='test_email'), #test email sending
    path('upload_resume/',upload_resume,name='resume_analyzer') ,#upload resume page
    path('resume_result/<int:pk>/',resume_result,name='resume_result') ,  #resume result page
    
    
]

