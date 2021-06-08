import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from school.email import EmailB
from django.core.files.storage import FileSystemStorage
from school.models import CustomUser, Staff, Courses, Subjects, Students


def home(request):
    return render(request, 'school/home.html')


def contact(request):
    return render(request, 'school/contact.html')


def loginpage(request):
    return render(request, 'school/loginpage.html')


def userdata(request):
    if request.user!=None:
        return HttpResponse("User "+request.user.email+" usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please log in")


def signin(request):
    if request.method!="POST":
        return HttpResponse("<h2> Wrong </h2>")
    else:
        user=EmailB.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/adminhome/')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse('staffhome'))
            else:
                return HttpResponseRedirect(reverse('studentshome'))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse("loginpage"))


def logoutpage(request):
    logout(request)
    return HttpResponseRedirect(reverse("loginpage"))

