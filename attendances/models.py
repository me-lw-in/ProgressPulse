from django.db import models
# from accounts.models import User_Data
from academics.models import *
from accounts.models import CustomUser

# Create your models here.

class AttendanceData(models.Model):                 #size of attributes have to be re-sized
    ATTENDANCE_STATUS_CHOICES = (
    ('P', 'Present'),
    ('A', 'Absent'),
    )
    
    attendance_id = models.AutoField(primary_key=True)
    registration_no = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance_records')
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records')
    section = models.CharField(max_length=10, default='0',null=True)     # 0-> no section, A->section A, B ->section B
    attendance_date = models.DateField()
    period = models.CharField(max_length=10, choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('morning', 'Morning'), ('afternoon', 'Afternoon')),default='0', null=False)
    attendance_status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS_CHOICES, default='A')
    subject_type = models.CharField(max_length=100, null=True)
    sem = models.CharField(max_length=1, choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')))
 
    
    def __str__(self):
        return f"{self.registration_no.username} - {self.registration_no.name} - {self.subject_code.subject_name} - {self.subject_code.year_id.year_name} - {self.attendance_date}"