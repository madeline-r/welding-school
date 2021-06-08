import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ckeditor.fields import RichTextField
from school.models import CustomUser, Staff, Courses, Subjects, Students, CourseTime, Materials, Attendance, AReport, Results, Informations

def staffhome(request):
    info=Informations.objects.all().order_by('-created_at')
    return render(request,'school/staff/staffhome.html',{"info":info})


def staffaddattendance(request):
    subjects=Subjects.objects.filter(staffid=request.user.id)
    coursetime=CourseTime.objects.all()
    return render(request,'school/staff/staffaddattendance.html',{"subjects":subjects,"coursetime":coursetime})


@csrf_exempt
def fetchstudents(request):
    subject_id=request.POST.get("subject")
    course_time=request.POST.get("time")

    subject=Subjects.objects.get(id=subject_id)
    time_model=CourseTime.objects.get(id=course_time)
    students=Students.objects.filter(courseid=subject.courseid,coursetimeid=time_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json", safe=False)


@csrf_exempt
def staffsaveattendance(request):
    studentids=request.POST.get("studentids")
    subject_id=request.POST.get("subject_id")
    attendancedate=request.POST.get("attendancedate")
    coursetime_id=request.POST.get("coursetime_id")
    subjectmodel=Subjects.objects.get(id=subject_id)
    timemodel=CourseTime.objects.get(id=coursetime_id)
    jsonstudent=json.loads(studentids)
    try:
        attendance=Attendance(subjectid=subjectmodel,attendancedate=attendancedate,coursetimeid=timemodel)
        attendance.save()
        for stud in jsonstudent:
            student=Students.objects.get(admin=stud['id'])
            areport=AReport(studentid=student,attendancetid=attendance,status=stud['status'])
            areport.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Err")


def staffmanageattendance(request):
    subjects=Subjects.objects.filter(staffid=request.user.id)
    coursetimeid=CourseTime.objects.all()   
    return render(request,"school/staff/staffmanageattendance.html",{"subjects":subjects,"coursetimeid":coursetimeid})


@csrf_exempt
def fetchattendancedates(request):
    subject=request.POST.get("subject")
    coursetimeid=request.POST.get("coursetimeid")
    subjectobject=Subjects.objects.get(id=subject)
    coursetimeobject=CourseTime.objects.get(id=coursetimeid)
    attendance=Attendance.objects.filter(subjectid=subjectobject,coursetimeid=coursetimeobject)
    attendanceobject=[]
    for singleattendance in attendance:
        data={"id":singleattendance.id,"attendancedate":str(singleattendance.attendancedate),"coursetimeid":singleattendance.coursetimeid.id}
        attendanceobject.append(data)
    return JsonResponse(json.dumps(attendanceobject),safe=False)


@csrf_exempt
def fetchattendancestudents(request):
    attendancedate=request.POST.get("attendancedate")
    attendance=Attendance.objects.get(id=attendancedate)
    attendancedata=AReport.objects.filter(attendancetid=attendance)
    list_data=[]
    for student in attendancedata:
        data_small={"id":student.studentid.admin.id,"name":student.studentid.admin.first_name+" "+student.studentid.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json", safe=False)


@csrf_exempt
def staffeditattendance (request):
    studentids=request.POST.get("studentids")
    attendancedate=request.POST.get("attendancedate")
    attendance=Attendance.objects.get(id=attendancedate)
    jsonstudent=json.loads(studentids)
    try:
        for stud in jsonstudent:
            student=Students.objects.get(admin=stud['id'])
            areport=AReport.objects.get(studentid=student,attendancetid=attendance)
            areport.status=stud['status']
            areport.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Err")


def staffaddmaterials(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subjects=Subjects.objects.filter(staffid=request.user.id)
    return render(request,'school/staff/staffaddmaterials.html',{"subjects":subjects, "staff_id":staff_id,})


def staffsavematerials(request):
    if request.method!='POST':
        return HttpResponseRedirect("Błąd")
    title=request.POST.get('title')
    content=request.POST.get('content')
    staff_obj=Staff.objects.get(admin=request.user.id)
    subject_id=request.POST.get('subject')
    subjectobject=Subjects.objects.get(id=subject_id)
    try:
        material=Materials(subjectid=subjectobject,staffid=staff_obj,title=title,content=content)
        material.save()
        messages.success(request, "Dodano materiał")
        return HttpResponseRedirect(reverse("staffaddmaterials"))
    except:
        messages.error(request, "Nie udało się dodać materiału")
        return HttpResponseRedirect(reverse("staffaddmaterials"))


def staffmanagematerials(request):
    staff_obj=Staff.objects.get(admin=request.user.id)
    materials=Materials.objects.filter(staffid=staff_obj)
    return render(request,'school/staff/staffmanagematerials.html',{"materials":materials,"staff_obj":staff_obj})


def staffmaterialcontent(request, material_id):
    material = Materials.objects.get(id = material_id)
    return render(request,"school/staff/staffmaterialcontent.html",{"material":material,"id":material_id})


def staffeditmaterial(request, material_id):
    material = Materials.objects.get(id = material_id)
    staff_id=Staff.objects.get(admin=request.user.id)
    subjects=Subjects.objects.filter(staffid=request.user.id)
    return render(request,"school/staff/staffeditmaterial.html",{"material":material, "subjects":subjects, "staff_id":staff_id, "id":material_id})


def staffeditsavematerial(request):
    if request.method!="POST":
        return HttpResponse("<h2>Error</h2>")
    else:
        material_id=request.POST.get("material_id")
        subjectid=request.POST.get("subject")
        title=request.POST.get("title")
        content=request.POST.get("content")
        try:
            material=Materials.objects.get(id=material_id)
            subject=Subjects.objects.get(id=subjectid)
            material.subjectid=subject
            material.title=title
            material.content=content
            material.save()
            messages.success(request,"Poprawnie zaktualizowano materiał")
            return HttpResponseRedirect(reverse("staffeditmaterial",kwargs={"material_id":material_id}))
        except:
            messages.error(request,"Błąd edycji materiału")
            return HttpResponseRedirect(reverse("staffeditmaterial",kwargs={"material_id":material_id}))


@csrf_exempt
def staffdeletematerial(request, material_id):
    material = Materials.objects.get(id = material_id)
    if request.method == "POST":
        material.delete()
        return redirect('/staffmanagematerials/')
    return render(request,"school/staff/staffdeletematerial.html",{"material":material, "id":material_id})
    

def staffprofile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"school/staff/staffprofile.html",{"user":user})


def staffprofileedit(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staffprofile"))
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
            return HttpResponseRedirect(reverse("staffprofile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staffprofile"))


def staffaddresults(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    result=Results.objects.all()
    subjects=Subjects.objects.filter(staffid=request.user.id)
    coursetime=CourseTime.objects.all()   
    return render(request,"school/staff/staffaddresults.html",{"staff_id":staff_id, "subjects":subjects,"coursetime":coursetime,"result":result})


def staffsaveresults(request):
    if request.method!='POST':
        return HttpResponseRedirect('staffaddresults/')
    staff_obj=Staff.objects.get(admin=request.user.id)
    student_id=request.POST.get('studentlist')
    materialresult=request.POST.get('materialresult')
    description=request.POST.get('description')
    subject_id=request.POST.get('subject')
    studentobject=Students.objects.get(admin=student_id)
    subjectobject=Subjects.objects.get(id=subject_id)
    try:
        check=Results.objects.filter(subjectid=subjectobject,studentid=studentobject).exists()
        if check:
            results=Results.objects.get(subjectid=subjectobject,studentid=studentobject)
            results.materialresult=materialresult
            results.description=description
            results.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("staffaddresults"))
        else:
            results=Results(staffid=staff_obj, studentid=studentobject,subjectid=subjectobject,materialresult=materialresult,description=description)
            results.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("staffaddresults"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("staffaddresults"))


def staffmanageresults(request):
    staff_obj=Staff.objects.get(admin=request.user.id)
    results=Results.objects.filter(staffid=staff_obj)
    return render(request,"school/staff/staffmanageresults.html",{"results":results,"staff_obj":staff_obj})





