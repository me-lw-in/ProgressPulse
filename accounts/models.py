from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        # Check if username is provided
        if not username:
            raise ValueError("Please provide a valid username")
        
        # Create a new user instance with the provided username and extra fields
        user = self.model(username=username, **extra_fields)
        
        # Set the user's password using the set_password method
        user.set_password(password)
        
        # Save the user instance to the database
        user.save(using=self._db)
        
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        # Set default values for is_staff and is_superuser fields
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        # Call the _create_user method to create a new user with the provided username, password, and extra fields
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        # Set default values for is_staff and is_superuser fields to True for superusers
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Call the _create_user method to create a new superuser with the provided username, password, and extra fields
        return self._create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Define the fields for the custom user model
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female')], null=False)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('student', 'Student'), ('teacher', 'Teacher')], blank=True)
    course_id = models.CharField(max_length=15, default='0', blank=True)   # if no values is given then it should store 0
    year_id = models.CharField(max_length=10, default='0', blank=True)    # if no values is given then it should store 0
    sem = models.CharField(max_length=10, choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('even', 'Even'),               # even & odd for teachers only
        ('odd', 'Odd'),
        ('passed out', 'Passed Out')    # passed_out -> for students who have passed from college (after third year)
        ], null=True, blank=True, default='0')
    language_pref = models.CharField(max_length=10, choices=[
        ('0', '0'),                     # 0 -> for teachers
        ('hindi', 'Hindi'),             
        ('kannada', 'Kannada'), 
        ('malayalam', 'Malayalam')
        ], null=True, blank=True,default='0')
    course_type = models.CharField(max_length=100, choices=[
        ('0', '0'),                                        # 0 -> means for teachers 
        ('normal', 'Normal'),                              # normal -> means for those students who dont have any add courses
        ('ai/ml', 'AI/ML and Big Data'),
        ('logistics', 'Supply Chain & Logistics'),
        ('aviation', 'Hospitality & Aviation')], null=True, blank=True,default='0')
    lab_batch_type = models.CharField(max_length=10, choices=[
        ('0', '0'),                                         #0 -> means for teachers and students if there is no lab batch
        ('normal', 'Normal'),            # change A and B to normal and addon
        ('addon', 'AddOn'),
        ], null=True, blank=True,default='0')
    
    section_id = models.CharField(max_length=1,choices=[
        ('0', '0'),                 # 0 -> for teachers and students who dont have any section
        ('A', 'A'),     
        ('B', 'B')
        ], null=True, blank=True,default='0')
    AdmissionYear = models.PositiveIntegerField(default=0, blank=True)  #if not there then it should store 0
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Set the custom user manager
    objects = CustomUserManager()
    
    # Specify the unique identifier field for authentication
    USERNAME_FIELD = 'username'
    
    # Specify the required fields for creating a user
    REQUIRED_FIELDS = ['name', 'email', 'gender', 'user_type']
    
    class Meta:
        # Set the verbose name and plural name for the model
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
    
    def get_full_name(self):
        # Return the full name of the user
        return self.name
    
    def get_short_name(self):
        # Return the short name of the user
        return self.name

    def __str__(self):
        return self.username+" - "+self.name+" - "+self.user_type






# Create your models here.

# =========users table=========

# class User_Data(AbstractBaseUser):
    

#     user_id = models.CharField(max_length=100, unique=True, primary_key=True)
#     name = models.CharField(max_length=100, null=False)  
#     email = models.EmailField(unique=True, null=False)
#     gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=False)
#     user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')], null=False)
#     course_id = models.CharField(max_length=10, null=True, blank=True)
#     year_id = models.CharField(max_length=10, null=True, blank=True)
#     sem = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], null=True, blank=True)
#     language_pref = models.CharField(max_length=10, choices=[('HINDI', 'Hindi'), ('KANNADA', 'Kannada'), ('MALAYALAM', 'Malayalam')], null=True, blank=True)
#     batch_type = models.CharField(max_length=100, null=True, blank=True)
#     AdmissionYear = models.PositiveIntegerField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)


#     def __str__(self):
#         return self.user_id+" - "+self.name+" - "+self.user_type+" - "+self.course_id+" - "+self.year_id






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
    