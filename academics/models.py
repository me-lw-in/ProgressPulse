from django.db import models
from accounts.models import *

#size of attributes of each models have to be resized
# Create your models here.

# ========Course table=======

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=15) #add same thing first year, second year, third year for all fields
    course_name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.course_id+" "+self.course_name

# ========Year table=======

class Year(models.Model):
    year_id = models.CharField(primary_key=True, max_length=15)
    year_name = models.CharField(max_length=15, null=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='years') # add first year, second year, third year for all fields

    def __str__(self):
        return self.year_id+" "+self.year_name



# ========Subject table=======

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=15, unique=True)
    subject_name = models.CharField(max_length=100, null=False)
    year_id = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='subjects')
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)  
    total_classes = models.PositiveIntegerField(null=False, default=0)
    section = models.CharField(max_length=10, default='0',null=True)     # 0-> no section, A->section A, B ->section B
    subject_type = models.CharField(
        max_length=100,
        choices=(
            ('normal theory', 'Normal Theory'),
            ('normal lab', 'Normal Lab'),
            ('ai/ml lab', 'Ai/Ml Lab'),
            ('ai/ml theory', 'Ai/Ml Theory'),
            ('logistics', 'Supply Chain & Logistics'),
            ('aviation', 'Aviation & Hospitality'),
            ('hindi', 'Hindi'),             
            ('kannada', 'Kannada')
        )
    )
    sem = models.CharField(
        max_length=1,
        choices=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        )
    )
    lab_batch_type = models.CharField(max_length=10, choices=(
        ('0', '0'),  # Default value for subjects without lab batch
        ('addon', 'Addon'),
        ('normal', 'Normal'),
    ), default='0')
    

    def __str__(self):
        return self.subject_code+"-"+self.subject_name+": "+self.subject_type+"- "+self.year_id.year_id
        

# ========Section table=======   # waste no use
# class Section(models.Model):
#     section_id = models.CharField(primary_key=True, max_length=10)
#     section_name = models.CharField(max_length=100, null=False)
#     year_id = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='sections')
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')

#     def __str__(self):
#         return self.section_id+" "+self.section_name


# ========TeacherSubject table=======

# class TeacherSubject(models.Model):
#     teachersubject_id = models.AutoField(primary_key=True)
#     teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_subjects', null=True)
#     subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_subjects')
#     # section_id = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='teacher_subjects')      # no need
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teacher_subjects')
#     sem = models.CharField(max_length=1, choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')))

#     def __str__(self):
#         return f"{self.teacher.username} - {self.subject.subject_name}"