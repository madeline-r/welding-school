import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from school.email import EmailB
from django.core.files.storage import FileSystemStorage

from school.models import CustomUser, Staff, Courses, Subjects, Students, Attendance, AReport, Results, Informations, Materials


def studentshome(request):
    info=Informations.objects.all().order_by('-created_at')
    return render(request,'school/students/studentshome.html',{"info":info})


def studentattendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.courseid
    subjects=Subjects.objects.filter(courseid=course)
    return render(request,'school/students/studentattendance.html',{"subjects":subjects})


def studentattendancepost(request):
    subjectid=request.POST.get("subject")
    startdate=request.POST.get("startdate")
    enddate=request.POST.get("enddate")
    startdataparse=datetime.datetime.strptime(startdate,"%Y-%m-%d").date()
    enddataparse=datetime.datetime.strptime(enddate,"%Y-%m-%d").date()
    subjectobject=Subjects.objects.get(id=subjectid)
    userobject=CustomUser.objects.get(id=request.user.id)
    studentobject=Students.objects.get(admin=userobject)
    attendance=Attendance.objects.filter(attendancedate__range=(startdataparse,enddataparse),subjectid=subjectobject)
    areports=AReport.objects.filter(attendancetid__in=attendance,studentid=studentobject)
    return render(request,'school/students/studentattendancedata.html',{"areports":areports})


def studentresults(request):
    student=Students.objects.get(admin=request.user.id)
    studentresults=Results.objects.filter(studentid=student.id)
    return render(request,'school/students/studentresults.html',{"studentresults":studentresults})


def studentprofile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"school/students/studentprofile.html",{"user":user})


def studentmaterials(request):
    materials=Materials.objects.all()
    return render(request,'school/students/studentmaterials.html',{"materials":materials})


def studentmaterialcontent(request, material_id):
    material = Materials.objects.get(id = material_id)
    return render(request,"school/students/studentmaterialcontent.html",{"material":material,"id":material_id})


def studentprofileedit(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("studentprofile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("studentprofile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("studentprofile"))
    





