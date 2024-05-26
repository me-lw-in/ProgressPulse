from django.urls import path
from .views import*

app_name = 'academics'

urlpatterns = [
  path('', path_redirector ,name='path_redirector'),
  path('student-dashboard/', student_dashboard ,name='student_dashboard'),
  path('teacher-dashboard/', teacher_dashboard ,name='teacher_dashboard'),
  path('logout_user/', logout_user ,name='logout_user'),
  path('change-password/',change_pass_in_dashboards , name='change-password'),
  path('otp-verification/',verify_otp , name='otp-verification'),
  path('create-password/',verify_password , name='create-password'),
   
    
]
