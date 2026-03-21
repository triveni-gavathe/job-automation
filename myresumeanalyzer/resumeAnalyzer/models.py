from django.db import models
from django.contrib.auth.models  import User
# Create your models here.
class Resume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='resumes/')
    extracted_text=models.TextField(blank=True)
    score=models.IntegerField(default=0)
    analysis=models.TextField(blank=True)
    uploaded_at=models.DateTimeField(auto_created=True)
    
    
    def __str__(self):
        return f"{self.user.username}- {self.uploaded_at}"
    
    
    