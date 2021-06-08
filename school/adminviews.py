import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from school.email import EmailB
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from school.models import CustomUser, Staff, Courses, Subjects, Students, CourseTime, Results, Informations

def adminhome(request):
    info=Informations.objects.all().order_by('-created_at')
    return render(request,'school/admin/adminhome.html',{"info":info})


def adminaddstaff(request):
    return render(request,'school/admin/adminaddstaff.html')


def adminsavestaff(request):
    if request.method!="POST":
        return HttpResponse("No.")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("adminaddstaff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("adminaddstaff"))


def adminmanagestaff(request):
    staff=Staff.objects.all()
    return render(request,"school/admin/adminmanagestaff.html",{"staff":staff})


def admineditstaff(request, staff_id):
    staff = Staff.objects.get(admin = staff_id)
    return render(request,"school/admin/admineditstaff.html",{"staff":staff,"id":staff_id})


def admineditsavestaff(request):
    if request.method!="POST":
        return HttpResponse("<h2> Error </h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            staffmodel=Staff.objects.get(admin=staff_id)
            staffmodel.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("admineditstaff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("admineditstaff",kwargs={"staff_id":staff_id}))


@csrf_exempt
def admindeletestaff(request, staff_id):
    staff = Staff.objects.get(admin = staff_id)
    if request.method == "POST":
        staff.delete()
        return redirect('/adminmanagestaff/')
    return render(request,"school/admin/admindeletestaff.html",{"staff":staff, "id":staff_id})


def adminaddstudent(request):
    courses=Courses.objects.all()
    coursetime=CourseTime.objects.all()
    return render(request,'school/admin/adminaddstudent.html',{"courses":courses,"coursetime":coursetime})


def adminsavestudent(request):
    if request.method!="POST":
        return HttpResponse("No.")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        courseid=request.POST.get("course")
        coursetimeid=request.POST.get("time")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            courseobj=Courses.objects.get(id=courseid)
            timeobj=CourseTime.objects.get(id=coursetimeid)
            user.students.courseid=courseobj
            user.students.coursetimeid=timeobj
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect(reverse("adminaddstudent"))
        except:
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect(reverse("adminaddstudent"))


def adminmanagestudents(request):
    students=Students.objects.all()
    return render(request,"school/admin/adminmanagestudents.html",{"students":students})


def admineditstudent(request, student_id):
    courses=Courses.objects.all()
    coursetime=CourseTime.objects.all()
    student = Students.objects.get(admin = student_id)
    return render(request,"school/admin/admineditstudent.html",{"student":student,"id":student_id,"courses":courses,"coursetime":coursetime})


def admineditsavestudent(request):
    if request.method!="POST":
        return HttpResponse("<h2> Error </h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        courseid=request.POST.get("course")
        coursetimeid=request.POST.get("time")
        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()
            studentmodel=Students.objects.get(admin=student_id)
            course=Courses.objects.get(id=courseid)
            time=CourseTime.objects.get(id=coursetimeid)
            studentmodel.courseid=course
            studentmodel.coursetimeid=time
            studentmodel.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("admineditstudent",kwargs={"student_id":student_id}))
        except:
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect(reverse("admineditstudent",kwargs={"student_id":student_id}))


@csrf_exempt
def adminusernameexist(request):
    username=request.POST.get("username")
    userobject=CustomUser.objects.filter(username=username).exists()
    if userobject:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def admindeletestudent(request, student_id):
    student = Students.objects.get(admin = student_id)
    if request.method == "POST":
        student.delete()
        return redirect('/adminmanagestudents/')
    return render(request,"school/admin/admindeletestudent.html",{"student":student, "id":student_id})


def adminaddcourse(request):
    return render(request,'school/admin/adminaddcourse.html')


def adminsavecourse(request):
    if request.method!="POST":
        return HttpResponseRedirect("No")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(coursename=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("adminaddcourse"))
        except:
            messages.error(request,"Failed to Add Course")
            return HttpResponseRedirect(reverse("adminaddcourse"))


def adminmanagecourses(request):
    courses=Courses.objects.all()
    return render(request,"school/admin/adminmanagecourses.html",{"courses":courses})


def admineditcourse(request, course_id):
    course = Courses.objects.get(id = course_id)
    return render(request,"school/admin/admineditcourse.html",{"course":course,"id":course_id})


def admineditsavecourse(request):
    if request.method!="POST":
        return HttpResponse("<h2> Error </h2>")
    else:
        course_id=request.POST.get("course_id")
        coursename=request.POST.get("course")
        try:
            course=Courses.objects.get(id=course_id)
            course.coursename=coursename
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("admineditcourse",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("admineditcourse",kwargs={"course_id":course_id}))


@csrf_exempt
def admindeletecourse(request, course_id):
    course = Courses.objects.get(id = course_id)
    if request.method == "POST":
        course.delete()
        return redirect('/adminmanagecourses/')
    return render(request,"school/admin/admindeletecourse.html",{"course":course, "id":course_id})


def adminaddsubject(request):
    courses=Courses.objects.all()
    staff=CustomUser.objects.filter(user_type=2)
    return render(request,'school/admin/adminaddsubject.html',{"staff":staff,"courses":courses})


def adminsavesubject(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subjectname=request.POST.get("subjectname")
        courseid=request.POST.get("course")
        course=Courses.objects.get(id=courseid)
        staffid=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staffid)
        try:
            subject=Subjects(subjectname=subjectname,courseid=course,staffid=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("adminaddsubject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("adminaddsubject"))


def adminmanagesubjects(request):
    subjects=Subjects.objects.all()
    return render(request,"school/admin/adminmanagesubjects.html",{"subjects":subjects})


def admineditsubject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staff=CustomUser.objects.filter(user_type=2)
    return render(request,"school/admin/admineditsubject.html",{"subject":subject,"staff":staff,"courses":courses,"id":subject_id})


def admineditsavesubject(request):
    if request.method!="POST":
        return HttpResponse("<h2>Error</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subjectname=request.POST.get("subjectname")
        staffid=request.POST.get("staff")
        courseid=request.POST.get("course")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subjectname=subjectname
            staff=CustomUser.objects.get(id=staffid)
            subject.staffid=staff
            course=Courses.objects.get(id=courseid)
            subject.courseid=course
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("admineditsubject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("admineditsubject",kwargs={"subject_id":subject_id}))


@csrf_exempt
def admindeletesubject(request, subject_id):
    subject = Subjects.objects.get(id = subject_id)
    if request.method == "POST":
        subject.delete()
        return redirect('/adminmanagesubjects/')
    return render(request,"school/admin/admindeletesubject.html",{"subject":subject, "id":subject_id})


def adminaddtime(request):
    return render(request,"school/admin/adminaddtime.html")


def adminsavetime(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("adminaddtime"))
    else:
        startcourse=request.POST.get("startcourse")
        endcourse=request.POST.get("endcourse")
        try:
            coursetime=CourseTime(startcourse=startcourse,endcourse=endcourse)
            coursetime.save()
            messages.success(request,"Successfully Added Course Time")
            return HttpResponseRedirect(reverse("adminaddtime"))
        except:
            messages.error(request,"Failed to Add Course Time")
            return HttpResponseRedirect(reverse("adminaddtime"))


def adminmanagetime(request):
    time=CourseTime.objects.all()
    return render(request,"school/admin/adminmanagetime.html",{"time":time})


def adminedittime(request, time_id):
    time = CourseTime.objects.get(id = time_id)
    return render(request,"school/admin/adminedittime.html",{"time":time,"id":time_id})


def admineditsavetime(request):
    if request.method!="POST":
        return HttpResponse("<h2> Error </h2>")
    else:
        time_id=request.POST.get("time_id")
        startcourse=request.POST.get("startcourse")
        endcourse=request.POST.get("endcourse")
        try:
            time=CourseTime.objects.get(id=time_id)
            time.startcourse=startcourse
            time.endcourse=endcourse
            time.save()
            messages.success(request,"Successfully Edited czas")
            return HttpResponseRedirect(reverse("adminedittime",kwargs={"time_id":time_id}))
        except:
            messages.error(request,"Failed to Edit czas")
            return HttpResponseRedirect(reverse("adminedittime",kwargs={"time_id":time_id}))


@csrf_exempt
def admindeletetime(request, time_id):
    time = CourseTime.objects.get(id = time_id)
    if request.method == "POST":
        time.delete()
        return redirect('/adminmanagetime/')
    return render(request,"school/admin/admindeletetime.html",{"time":time, "id":time_id})


def adminmanageresults(request):
    results=Results.objects.all()
    return render(request,"school/admin/adminmanageresults.html",{"results":results})


@csrf_exempt
def admindeleteresult(request, result_id):
    result = Results.objects.get(id = result_id)
    if request.method == "POST":
        result.delete()
        return redirect('/adminmanageresults/')
    return render(request,"school/admin/admindeleteresult.html",{"result":result, "id":result_id})


def adminaddinformation(request):
    return render(request,'school/admin/adminaddinformation.html')


def adminsaveinformation(request):
    if request.method!="POST":
        return HttpResponseRedirect("Błąd")
    else:
        title=request.POST.get('title')
        content=request.POST.get('content')
        try:
            info=Informations(title=title,content=content)
            info.save()
            messages.success(request, "Dodano informacje")
            return HttpResponseRedirect(reverse("adminaddinformation"))
        except:
            messages.error(request, "Nie udało się dodać informacji")
            return HttpResponseRedirect(reverse("sadminaddinformation"))


def adminmanageinformations(request):
    info=Informations.objects.all()
    return render(request,"school/admin/adminmanageinformations.html",{"info":info})


def admineditinformation(request, info_id):
    info = Informations.objects.get(id = info_id)
    return render(request,"school/admin/admineditinformation.html",{"info":info,"id":info_id})


def admineditsaveinformation(request):
    if request.method!="POST":
        return HttpResponse("<h2> Error </h2>")
    else:
        info_id=request.POST.get("info_id")
        title=request.POST.get('title')
        content=request.POST.get('content')
        try:
            info=Informations.objects.get(id=info_id)
            info.title=title
            info.content=content
            info.save()
            messages.success(request,"Zaktualizowano informacje")
            return HttpResponseRedirect(reverse("admineditinformation",kwargs={"info_id":info_id}))
        except:
            messages.error(request,"Nie udało sie zaktualizować informacji")
            return HttpResponseRedirect(reverse("admineditinformation",kwargs={"info_id":info_id}))


@csrf_exempt
def admindeleteinformation(request, info_id):
    info = Informations.objects.get(id = info_id)
    if request.method == "POST":
        info.delete()
        return redirect('/adminmanageinformations/')
    return render(request,"school/admin/admindeleteinformation.html",{"info":info, "id":info_id})


def adminprofile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"school/admin/adminprofile.html",{"user":user})    


def adminprofileedit(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("adminprofile"))
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
            return HttpResponseRedirect(reverse("adminprofile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("adminprofile"))