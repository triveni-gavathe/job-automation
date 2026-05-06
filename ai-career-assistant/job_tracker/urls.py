from django.urls import path
from .views import *
urlpatterns=[
    path('job_home',job_home,name='job_home'),
]