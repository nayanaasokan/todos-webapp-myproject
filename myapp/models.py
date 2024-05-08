from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Task(models.Model):
    
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    status_options=(
        ("completed","completed"),
        ("pending","pending")
        )
    status=models.CharField(max_length=200,choices=status_options,default="pending")
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)

    def __str__(self):
        return self.title 
