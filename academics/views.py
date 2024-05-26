import random
from django.core.cache import cache
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
# from accounts.models import User_Data
from academics.models import Subject
from accounts.models import CustomUser
from attendances.models import AttendanceData
from django.db.models import Case, Value, When, BooleanField, Q
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def path_redirector(request):
    
    if request.user.is_anonymous:
        return redirect('accounts:login')
    else:
        username = request.user.username
        if CustomUser.objects.filter(username=username, user_type = 'student').exists():
            return redirect('/student-dashboard')
        elif CustomUser.objects.filter(username=username, user_type = 'teacher').exists():
            return redirect('/teacher-dashboard')
        else:
            return redirect('accounts:login')



def student_dashboard(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        student = request.user
        print(student)

        # Use a dictionary to map course codes to course names
        course_mapping = {
            'BCA': 'Bachelor of Computer Application',
            'BCOM': 'Bachelor of Commerce',
            'BBA': 'Bachelor of Business Administration'
        }
        
        # Get the course name based on the student's course code
        course_name = course_mapping.get(student.course_id, 'Unknown')

        subjects = Subject.objects.filter(sem = student.sem, year_id=student.year_id, )
        print('\n')
        print(subjects)
        print('\n')

        theory_subject = subjects.filter(section=student.section_id, subject_type= 'normal theory').order_by('subject_name')
        print('theoery-',theory_subject)
        print('\n')
        theory_subject_attendance = []
        for theory_sub in theory_subject:
            attendance_count = AttendanceData.objects.filter(
                registration_no=student,
                subject_code=theory_sub,
                attendance_status='P'
                ).count()
            theory_subject_attendance.append({
                'subject': theory_sub,
                'attendance_count': attendance_count
                })


        print(theory_subject_attendance)
        print('\n')
        for attendance in theory_subject_attendance:
            print(attendance)

        print("Total - ",theory_subject_attendance)

        lab_subject_attendance = []
        if student.lab_batch_type != '0':
            lab_batch = student.lab_batch_type
            lab_subject = subjects.filter(lab_batch_type=lab_batch).order_by('subject_name')
            for subject in lab_subject:
                attendance_count = AttendanceData.objects.filter(
                    registration_no=student,
                    subject_code=subject,
                    attendance_status='P'
                ).count()
                lab_subject_attendance.append({
                    'subject': subject,
                    'attendance_count': attendance_count
                })


            print(lab_subject)
            print('\n')
            print(lab_subject_attendance)
            

        else:
            try:
                lab_subject=subjects.filter(lab_batch_type='0',subject_type='normal lab').order_by('subject_name')
                for subject in lab_subject:
                    attendance_count = AttendanceData.objects.filter(
                        registration_no=student,
                        subject_code=subject,
                        attendance_status='P'
                    ).count()
                    lab_subject_attendance.append({
                        'subject': subject,
                        'attendance_count': attendance_count
                    })
            except:
                lab_subject = 'no_lab_subjects'
                lab_subject_attendance = []

        print(lab_subject)
        print('\n')
        print(lab_subject_attendance)
            
        

        print(student.language_pref,'\n')

        lang_subject_attendance = []
        if student.language_pref != '0':
            lang_subject = subjects.filter(subject_type=student.language_pref).order_by('subject_name')
            for subject in lang_subject:
                attendance_count = AttendanceData.objects.filter(
                    registration_no = student,
                    subject_code = subject,
                    attendance_status = 'P'
                ).count()
                lang_subject_attendance.append({
                    'subject': subject,
                    'attendance_count': attendance_count
                })
        else:
            lang_subject = 'no_language_subjects'
            lang_subject_attendance = []
        print('lang:-',lang_subject_attendance)
       
        context = {
            'student': student,
            'course_name':course_name,
            'theory_subject':theory_subject,
            'lang_subject':lang_subject,
            'lab_subject':lab_subject,
            'theory_subject_attendance':theory_subject_attendance,
            'lang_subject_attendance':lang_subject_attendance,
            'lab_subject_attendance':lab_subject_attendance,
        }

        return render(request, 'academics/student-dashboard.html', context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
            return redirect('/teacher-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
    

def teacher_dashboard(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():

        teacher = request.user
        teacher_sem = teacher.sem

        # Filter subjects based on the user's current semester
        if teacher_sem in ['even']:
            subjects = Subject.objects.filter(teacher_id=teacher, sem__in=['2', '4', '6']).order_by('year_id')
        elif teacher_sem in ['odd']:
            subjects = Subject.objects.filter(teacher_id=teacher, sem__in=['1', '3', '5']).order_by('year_id')
        
        # Annotate subjects with display flag 
        subjects = subjects.annotate(
            is_normal_lab=Case(
                When(subject_type='normal lab', then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            display_section=Case(
                When(section='0', then=Value(False)),
                default=Value(True),
                output_field=BooleanField()
            ),
            display_lab_batch=Case(
                When(Q(subject_type='normal lab') & ~Q(lab_batch_type='0'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('year_id', 'section')

        context = {
            'teacher': teacher,
            'subjects':subjects
        }


        return render(request,'academics/teacher-dashboard.html', context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('/student-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
       

def change_pass_in_dashboards(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif not request.user.is_anonymous:
        if request.method == 'POST':
            email = request.POST.get('email')
            print(email)

            if CustomUser.objects.filter(username = request.user.username,email = email).exists():
                otp = str(random.randint(111111, 999999))
                print(otp)
                cache_key = f'otp_{email}'
                cache.set(cache_key, otp, timeout=600)  # OTP expires in 10 minutes
  
                subject = "OTP for password reset"
                message = f"Your OTP is: {otp}\n\nPlease note that this OTP will expire in 10 minutes."
                from_email = settings.EMAIL_HOST_USER
                recipient_email = [email]
                send_mail(subject,message,from_email,recipient_email)
                print('\n ME')
                return render(request, 'academics/otp_new_password.html' )
            
            else:
                error_message = "Wrong email!"
                return render(request, 'academics/change_password.html', {'message': error_message})            

        return render(request, 'academics/change_password.html')
    else:
        return redirect('accounts:login')
    

def verify_otp(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif not request.user.is_anonymous:
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')
            cache_key =  f'otp_{request.user.email}'
            print(cache_key)
            stored_otp = cache.get(cache_key)
            print(stored_otp)
            if stored_otp is not None:
                if entered_otp == stored_otp:
                    print('\n win')
                    return render(request, 'academics/otp_new_password.html',{'success': True})
                else:
                    error_message = "Incorrect otp. Please try again!"
                    return render(request, 'academics/otp_new_password.html',{'message': error_message, 'success': False})
            else:
                # error_message = "Otp expired!"
                return redirect('academics:change-password')
        else:
            return redirect('academics:change-password')
    else:
        return redirect('accounts:login')

def verify_password(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username=request.user.username, user_type='teacher').exists():
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            user = CustomUser.objects.get(username=request.user.username)
            if password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                return redirect('academics:teacher_dashboard')
            else:
                error_message = "Passwords do not match. Please try again."
                return render(request, 'academics/otp_new_password.html', {'message': error_message, 'success': True})
        else:
            return redirect('academics:change-password')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username=request.user.username, user_type='student').exists():
        return redirect('academics:student_dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username=request.user.username, user_type='admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')

def logout_user(request):
    logout(request)
    return redirect('accounts:login')


