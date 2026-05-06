from django.db import models
from django.contrib.auth.models import User
# Create your models he

class job(models.Model):
    title=models.CharField(max_length=200)
    company=models.CharField( max_length=200)
    location=models.CharField(max_length=200)
    link=models.URLField(max_length=700)
    source=models.CharField(max_length=300)
    found_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}-{self.company}"
    
    
#db forthe aplications
class Application(models.Model):
    STATUS_CHOICES=[
        ('saved','Saved'),
        ('applied','Applied'),
        ('interview','Interview'),
        ('rejected','Rejected'),
        ('offer','Offer'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(job,on_delete=models.CASCADE)
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='saved'
        
    )
    applied_date=models.DateField(auto_now_add=True)
    notes=models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.job.title}-{
            self.status}"
#for the job alert 
             
class jobAlert(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    keyword=models.CharField(max_length=200) 
    location=models.CharField(max_length=200)    
    active=models.BooleanField(default=True)   
    def __str__(self):
        return f"{self.user.username} - {self.keyword}"