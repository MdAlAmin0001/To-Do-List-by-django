from django.db import models
from django.contrib.auth.models import AbstractUser



class Custom_user(AbstractUser):
    USER =[
        ('admin','Admin'),
        ('user','User'),
        
    ]
    
    user_type=models.CharField(choices=USER, max_length=50)
    username=models.CharField(null=True, blank=True, max_length=50, unique=True)
    email=models.EmailField(unique=True, max_length=100)
    display_name=models.CharField(max_length=50, null=True, blank=True)
    password=models.CharField(max_length=50) 
    otp_token = models.CharField(max_length = 6, blank = True, null = True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    
    def __str__(self):
        return self.username
    
class Task(models.Model):
    user = models.ForeignKey(Custom_user, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], default='HIGH')
    is_completed = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    scheduled_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['priority', 'is_completed', 'due_date']
