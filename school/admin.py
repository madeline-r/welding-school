from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from school.models import CustomUser

# Register your models here.
# admin.site.register(Student)

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)