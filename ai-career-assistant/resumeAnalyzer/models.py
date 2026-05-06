from django.db import models
from django.contrib.auth.models  import User
from django.utils import timezone
# Create your models here.
class Resume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='resumes/')
    extracted_text=models.TextField(blank=True)
    score=models.IntegerField(default=0)
    analysis=models.TextField(blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.username}- {self.uploaded_at}"
    
class OTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    otp_code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    is_used=models.BooleanField(default=False)


    def is_expired(self):
        #otp expire after 10 mintutes
        return timezone.now()>self.created_at + timezone.timedelta(minutes=10)
    def __str__(self):
        return f"{self.user.username}-{self.otp_code}"

class JobMatchAnalysis(models.Model):
    resume=models.ForeignKey(Resume,on_delete=models.CASCADE)
    job_description=models.TextField()
    match_score=models.IntegerField(default=0)
    missing_skills=models.TextField(blank=True)
    analyzed_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.match_score}%-{self.analyzed_at}"
        