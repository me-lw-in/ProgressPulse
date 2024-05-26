from django.db import models
from django.contrib.auth.models import AbstractBaseUser

 

# Create your models here.

# =========users table=========

class User_Data(AbstractBaseUser):
    

    user_id = models.CharField(max_length=100, unique=True, primary_key=True)
  
    name = models.CharField(max_length=100, null=False)  
    email = models.EmailField(unique=True, null=False)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=False)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')], null=False)
    course_id = models.CharField(max_length=10, null=True, blank=True)
    year_id = models.CharField(max_length=10, null=True, blank=True)
    sem = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], null=True, blank=True)
    language_pref = models.CharField(max_length=10, choices=[('HINDI', 'Hindi'), ('KANNADA', 'Kannada'), ('MALAYALAM', 'Malayalam')], null=True, blank=True)
    batch_type = models.CharField(max_length=100, null=True, blank=True)
    AdmissionYear = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user_id+" - "+self.name+" - "+self.user_type+" - "+self.course_id+" - "+self.year_id






# class Attendance(models.Model):
#     STATUS_CHOICES = [
#         ('P', 'Present'),
#         ('A', 'Absent'),
#     ]

#     registration_no = models.CharField(max_length=12)
#     section_id = models.CharField(max_length=5)
#     subject_id = models.CharField(max_length=5)
#     date = models.DateField()
#     period = models.IntegerField()
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     course_id = models.CharField(max_length=5)  

#     #shows registration numer 
#     def __str__(self):
#         return self.registration_no+" - "+self.subject_id+" : "+self.date.strftime("%d/%m/%Y")
    