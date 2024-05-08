from django.shortcuts import render,redirect
from myapp.models import Task
from myapp.forms import RegistrationForm,LoginForm,TaskForm
from django.views.generic import View
from django.contrib.auth import login,authenticate,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from myapp.decorator import signin_required
from django.contrib import messages
from django.db.models import Count


# Create your views here.


# url-localhost:8000/myapp/register/
# method-get,post


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration successful")
            return redirect("signin")
        messages.error(request,"invalid")
        return render(request,"register.html",{"form":form})
    
# url-localhost:8000/myapp/login/
# method-get,post

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,"login successful")
                return redirect("task-list")
        messages.error(request,"invalid")
        return render(request,"login.html",{"form":form})
    
# url-localhost:8000/myapp/logout/
# method-get

@method_decorator([signin_required,never_cache],name="dispatch")    
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"You logged out of session")
        return redirect("signin")



# url-localhost:8000/myapp/tasks/add/
# method-get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,"you added a task")
            return redirect("task-list")
        messages.error(request,"invalid")
        return render(request,"task_add.html",{"form":form})
    

# url-localhost:8000/myapp/tasks/all/
# method-get

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.filter(user_object=request.user)
        qs_1=qs.values("status").annotate(status_count=Count("status"))
        qs_2=Task.objects.filter(user_object=request.user,status='completed')
        return render(request,"task_list.html",{"data":qs,"data_1":qs_1,"data_2":qs_2})
    


# url-localhost:8000/myapp/tasks/id/
# method-get


@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,"task_detail.html",{"data":qs})


# url-localhost:8000/myapp/tasks/id/change/
# method-get,post


@method_decorator([signin_required,never_cache],name="dispatch")
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        form=TaskForm(instance=qs)
        return render(request,"task_update.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request,"you updated a task")
            return redirect("task-list")
        messages.success(request,"invalid")
        return render(request,"task_update.html",{"form":form})
    
# url-localhost:8000/myapp/tasks/id/remove/
# method-get

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.get(id=id).delete()
        messages.success(request,"one task deleted")
        return redirect("task-list")


# url-localhost:8000/myapp/tasks/summary/
# method-get
class SummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.filter(user_object=request.user,status='completed')
        qs_1=Task.objects.filter(user_object=request.user,status='pending')
        qs_2=Task.objects.filter(user_object=request.user,status='completed').aggregate(com_count=Count("status"))
        qs_3=Task.objects.filter(user_object=request.user).values("status").aggregate(task_count=Count("status"))
        return render(request,"summary.html",{"data":qs,"data_1":qs_1,"data_2":qs_2,"total_task":qs_3})



    
