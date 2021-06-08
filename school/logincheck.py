from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

class LoginCheck(MiddlewareMixin):
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "school.adminviews":
                    pass
                elif modulename == "school.views":
                    pass
                else: 
                    return HttpResponseRedirect(reverse("adminhome"))
            elif user.user_type == "2":
                if modulename == "school.staffviews":
                    pass
                elif modulename == "school.views":
                    pass
                else: 
                    return HttpResponseRedirect(reverse("staffhome"))
            elif user.user_type == "3":
                if modulename == "school.studentsviews":
                    pass
                elif modulename == "school.views":
                    pass
                else: 
                    return HttpResponseRedirect(reverse("studentshome"))
            else:
                modulename == "school.views"
        else:
            if request.path == reverse("loginpage") or request.path == reverse("signin") or modulename == "django.contrib.auth.views" or request.path == reverse("home") or request.path == reverse("contact"):
                pass
            else:
                return HttpResponseRedirect(reverse("loginpage"))