from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import LoginForm,UserEditForm
# Create your views here.


def user_login(request):
    if request.user.is_authenticated == True:
        return redirect("home:main")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user=User.objects.get(username=form.cleaned_data.get("username"))
            login(request,user)
            return redirect("home:main")

    else:
        form=LoginForm()
    return render(request,"account/login.html",{"form":form})



def user_logout(request):
    logout(request)
    return redirect("home:main")
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("password2")
        user = User.objects.create(username=username,email=email,password=pass1)
        login(request,user)
        return redirect("home:main")
    return render(request,"account/register.html")


def edit(request):
    user=request.user
    form=UserEditForm(instance=user)
    if request.method == "POST":
        form=UserEditForm(instance=user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:edit")

    return render(request,"account/edit.html",{"form":form})