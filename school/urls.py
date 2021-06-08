from django.urls import path, include
from . import views, adminviews, staffviews, studentsviews


urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('userdata/', views.userdata),
    path('signin/', views.signin, name="signin"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logoutpage/', views.logoutpage, name="logoutpage"),


    path('adminhome/', adminviews.adminhome, name="adminhome"),

    path('adminprofile/', adminviews.adminprofile, name="adminprofile"),
    path('adminprofileedit/', adminviews.adminprofileedit, name="adminprofileedit"),


    path('adminaddstaff/', adminviews.adminaddstaff, name="adminaddstaff"),
    path('adminsavestaff/', adminviews.adminsavestaff, name="adminsavestaff"),
    path('adminmanagestaff/', adminviews.adminmanagestaff, name="adminmanagestaff"),
    path('admineditstaff/<str:staff_id>', adminviews.admineditstaff, name="admineditstaff"),
    path('admineditsavestaff/', adminviews.admineditsavestaff, name="admineditsavestaff"),
    path('admindeletestaff/<str:staff_id>', adminviews.admindeletestaff, name="admindeletestaff"),


    path('adminaddstudent/', adminviews.adminaddstudent, name="adminaddstudent"),
    path('adminusernameexist/', adminviews.adminusernameexist, name="adminusernameexist"),
    path('adminsavestudent/', adminviews.adminsavestudent, name="adminsavestudent"),
    path('adminmanagestudents/', adminviews.adminmanagestudents, name="adminmanagestudents"),
    path('admineditstudent/<str:student_id>', adminviews.admineditstudent,name="admineditstudent"),
    path('admineditsavestudent/', adminviews.admineditsavestudent,name="admineditsavestudent"),
    path('admindeletestudent/<str:student_id>', adminviews.admindeletestudent, name="admindeletestudent"),



    path('adminaddcourse/', adminviews.adminaddcourse, name="adminaddcourse"),
    path('adminsavecourse/', adminviews.adminsavecourse, name="adminsavecourse"),
    path('adminmanagecourses/', adminviews.adminmanagecourses, name="adminmanagecourses"),
    path('admineditcourse/<str:course_id>', adminviews.admineditcourse,name="admineditcourse"),
    path('admineditsavecourse/', adminviews.admineditsavecourse,name="admineditsavecourse"),
    path('admindeletecourse/<str:course_id>', adminviews.admindeletecourse, name="admindeletecourse"),


    path('adminaddsubject/', adminviews.adminaddsubject, name="adminaddsubject"),
    path('adminsavesubject/', adminviews.adminsavesubject, name="adminsavesubject"),
    path('adminmanagesubjects/', adminviews.adminmanagesubjects, name="adminmanagesubjects"),
    path('admineditsubject/<str:subject_id>', adminviews.admineditsubject,name="admineditsubject"),
    path('admineditsavesubject/', adminviews.admineditsavesubject,name="admineditsavesubject"),
    path('admindeletesubject/<str:subject_id>', adminviews.admindeletesubject, name="admindeletesubject"),


    path('adminaddtime/', adminviews.adminaddtime, name="adminaddtime"),
    path('adminsavetime/', adminviews.adminsavetime, name="adminsavetime"),
    path('adminmanagetime/', adminviews.adminmanagetime, name="adminmanagetime"),
    path('adminedittime/<str:time_id>', adminviews.adminedittime,name="adminedittime"),
    path('admineditsavetime/', adminviews.admineditsavetime,name="admineditsavetime"),
    path('admindeletetime/<str:time_id>', adminviews.admindeletetime, name="admindeletetime"),

    path('adminmanageresults/', adminviews.adminmanageresults, name="adminmanageresults"),
    path('admindeleteresult/<str:result_id>', adminviews.admindeleteresult, name="admindeleteresult"),

    path('adminaddinformation/', adminviews.adminaddinformation, name="adminaddinformation"),
    path('adminsaveinformation/', adminviews.adminsaveinformation, name="adminsaveinformation"),
    path('adminmanageinformations/', adminviews.adminmanageinformations, name="adminmanageinformations"),
    path('admineditinformation/<str:info_id>', adminviews.admineditinformation,name="admineditinformation"),
    path('admineditsaveinformation/', adminviews.admineditsaveinformation,name="admineditsaveinformation"),
    path('admindeleteinformation/<str:info_id>', adminviews.admindeleteinformation, name="admindeleteinformation"),



    path('staffhome/', staffviews.staffhome, name="staffhome"),

    path('staffprofile/', staffviews.staffprofile, name="staffprofile"),
    path('staffprofileedit/', staffviews.staffprofileedit, name="staffprofileedit"),

    path('staffaddattendance/', staffviews.staffaddattendance, name="staffaddattendance"),
    path('fetchstudents/', staffviews.fetchstudents, name="fetchstudents"),
    path('staffsaveattendance/', staffviews.staffsaveattendance, name="staffsaveattendance"),
    path('staffmanageattendance/', staffviews.staffmanageattendance, name="staffmanageattendance"),
    path('fetchattendancedates/', staffviews.fetchattendancedates, name="fetchattendancedates"),
    path('fetchattendancestudents/', staffviews.fetchattendancestudents, name="fetchattendancestudents"),
    path('staffeditattendance/', staffviews.staffeditattendance, name="staffeditattendance"),

    path('staffaddmaterials/', staffviews.staffaddmaterials, name="staffaddmaterials"),
    path('staffsavematerials/', staffviews.staffsavematerials, name="staffsavematerials"),
    path('staffmanagematerials/', staffviews.staffmanagematerials, name="staffmanagematerials"),
    path('staffmaterialcontent/<str:material_id>', staffviews.staffmaterialcontent, name="staffmaterialcontent"),
    path('staffeditmaterial/<str:material_id>', staffviews.staffeditmaterial, name="staffeditmaterial"),
    path('staffeditsavematerial/', staffviews.staffeditsavematerial, name="staffeditsavematerial"),
    path('staffdeletematerial/<str:material_id>', staffviews.staffdeletematerial, name="staffdeletematerial"),

    path('staffaddresults/', staffviews.staffaddresults, name="staffaddresults"),
    path('staffsaveresults/', staffviews.staffsaveresults, name="staffsaveresults"),
    path('staffmanageresults/', staffviews.staffmanageresults, name="staffmanageresults"),



    path('studentshome/', studentsviews.studentshome, name="studentshome"),

    path('studentprofile/', studentsviews.studentprofile, name="studentprofile"),
    path('studentprofileedit/', studentsviews.studentprofileedit, name="studentprofileedit"),

    path('studentattendance/', studentsviews.studentattendance, name="studentattendance"),
    path('studentattendancepost/', studentsviews.studentattendancepost, name="studentattendancepost"),

    path('studentmaterials/', studentsviews.studentmaterials, name="studentmaterials"),
    path('studentmaterialcontent/<str:material_id>', studentsviews.studentmaterialcontent, name="studentmaterialcontent"),

    path('studentresults/', studentsviews.studentresults, name="studentresults"),
]