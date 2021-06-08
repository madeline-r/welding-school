from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField


class CourseTime(models.Model):
    id=models.AutoField(primary_key=True)
    startcourse=models.DateField()
    endcourse=models.DateField()
    objects=models.Manager()


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1, choices=user_type_data,max_length=10)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Staff(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    coursename=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subjectname=models.CharField(max_length=100)
    courseid=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staffid=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    

class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    courseid=models.ForeignKey(Courses,on_delete=models.CASCADE)
    coursetimeid=models.ForeignKey(CourseTime, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Materials(models.Model):
    id=models.AutoField(primary_key=True)
    subjectid=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    staffid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    content=RichTextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subjectid=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    attendancedate=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    coursetimeid=models.ForeignKey(CourseTime, on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class AReport(models.Model):
    id=models.AutoField(primary_key=True)
    attendancetid=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    studentid=models.ForeignKey(Students,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Results(models.Model):
    id=models.AutoField(primary_key=True)
    staffid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    studentid=models.ForeignKey(Students,on_delete=models.CASCADE)
    subjectid=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    materialresult=models.FloatField(default=0)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Informations(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=300)
    content=models.CharField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


# Add date created
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staff.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance,courseid=Courses.objects.get(id=1),coursetimeid=CourseTime.objects.get(id=1))

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staff.save()
    if instance.user_type==3:
        instance.students.save()









    