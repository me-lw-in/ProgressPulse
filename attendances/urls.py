from django.urls import path
from .views import*

app_name = 'attendances'

urlpatterns = [
 path('take-attendance/<str:subject_code>/', student_details, name='take-attendance'),
 path('submit-attendance/',store_attendance, name='submit-attendance'),
 path('check-attendance/',subject_list_to_check_attendance_for_teachers, name='check-attendance'),     # for teacher's or teacher dasboard
 path('attendance-summary/<str:subject_code>/',attendace_summary_teachers, name='attendance-summary'),       # for teacher's or teacher dasboard
 path('attendance-history/',attendance_data_for_students, name='attendance-history'),     # for student's to check attendance history

#  path('check-attendance-data/',subject_list_to_check_attendance_for_students, name='check-attendance-data'),     # for student's or student dasboard
 
    
]

  