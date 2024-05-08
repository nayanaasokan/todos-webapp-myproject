from myapp.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Password")
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"})
            }
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=["title","description","status"]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control"})       
            }