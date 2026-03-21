from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('resume_analyzer/',resume_analyzer,name='resume_analyzer')
]