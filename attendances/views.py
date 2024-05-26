from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from academics.models import Subject
from .models import AttendanceData
from accounts.models import CustomUser
from datetime import date
import json
from django.db.models import Case, Value, When, BooleanField, Q
from django.db import models

# Create your views here.

# =====get class details=====
def student_details(request,subject_code):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
        teacher = request.user
        subject = get_object_or_404(Subject, subject_code=subject_code)
        
        if subject.subject_type == 'normal lab':
            if subject.lab_batch_type == '0':
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name).order_by('username')
            elif subject.lab_batch_type == 'normal':
                students = CustomUser.objects.filter(lab_batch_type='normal',year_id=subject.year_id.year_name).order_by('username')
            elif subject.lab_batch_type == 'addon':
                students = CustomUser.objects.filter(lab_batch_type='addon',year_id=subject.year_id.year_name).order_by('username')

            context = {
                'teacher': teacher,
                'subject': subject,
                'students': students,
                'success': True
            }
            return render(request,'attendances/take_attendance.html',context)

        elif subject.subject_name in ['kannada', 'hindi', 'malayalam']:
            if subject.section in ['A', 'B']:
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, language_pref=subject.subject_name, section_id=subject.section).order_by('username')
            else:
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, language_pref=subject.subject_name).order_by('username')
       
        elif subject.subject_type == 'normal theory':
            if subject.section == '0':
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name).order_by('username')
            else:
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, section_id=subject.section).order_by('username')
        elif subject.subject_type == 'aviation':
            students = CustomUser.objects.filter(year_id=subject.year_id.year_name, course_type='aviation').order_by('username')
        elif subject.subject_type == 'logistics':
            students = CustomUser.objects.filter(year_id=subject.year_id.year_name, course_type='logistics').order_by('username')   
        context = {
            'teacher': teacher,
            'subject': subject,
            'students': students,
            'success': False
        }
        return render(request, 'attendances/take_attendance.html', context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('academics:student_dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
    

# ====== code for storing submitted attendance data in the server ======

def store_attendance(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
        if request.method == 'POST':
            teacher = request.user
            attendance_data_json = request.POST.get('attendance_data')
            attendance_data = json.loads(attendance_data_json)
            selected_period = request.POST.get('period')
            teacher_date_str = request.POST.get('teacher_date')
            print(teacher_date_str)

            subject_sem = request.POST.get('subject_sem')
            subject_type = request.POST.get('subject_type')
            subject_code = request.POST.get('subject_code')
            total_classes = int(request.POST.get('total_classes'))      # Convert to integer
            print(total_classes)
            teacher_date_str = teacher_date_str.split('T')[0]  # Remove the time part
            teacher_date = date.fromisoformat(teacher_date_str)  # Convert to date object
            print(teacher_date)

            subject_code_name = get_object_or_404(Subject, subject_code=subject_code)
            section = subject_code_name.section
            

            for student_data in attendance_data:
                registration_no = student_data['registration_no']
                attendance_status = student_data['attendance_status']
                student = CustomUser.objects.get(username=registration_no)

                if AttendanceData.objects.filter(registration_no=student,subject_code=subject_code_name,attendance_date=teacher_date,period=selected_period,).exists():
                    print("Record already exists!")

                else:
                    attendance_record = AttendanceData.objects.create(
                        registration_no=student,
                        subject_code=subject_code_name,
                        attendance_date=teacher_date,
                        attendance_status=attendance_status,
                        subject_type=subject_type,
                        sem=subject_sem,
                        period=selected_period,
                        section=section
                    )
                    attendance_record.save()
                    # Increment the total_classes field for the subject
                    subject_code_name.total_classes = total_classes + 1
                    subject_code_name.save()
                    print(subject_code_name.total_classes)

            #Get attendance data

            attendance_summary = AttendanceData.objects.filter(
                subject_code=subject_code_name,
                attendance_date=teacher_date,
                period=selected_period,
                section=section
            )
            total_students = attendance_summary.count()

            # Get attendance data for present students
            present_students = attendance_summary.filter(
                subject_code=subject_code_name,
                attendance_date=teacher_date,
                period=selected_period,
                attendance_status='P'
            )
            total_present = present_students.count()

            # Get attendance data for absent students
            absent_students = attendance_summary.filter(
                subject_code=subject_code_name,
                attendance_date=teacher_date,
                period=selected_period,
                attendance_status='A'
            )
            total_absent = absent_students.count()

            try:
                # Render the template with attendance_submitted context
                # context = {'subject_instance': subject_code_name, 'total_students': total_students}
                context = {
                'total_students': total_students,
                'teacher': teacher,
                'total_present': total_present,
                'total_absent': total_absent,
                'present_students': present_students,
                'absent_students': absent_students,
                    }
                return render(request, 'attendances/attendace_download.html', context)
            except Exception as e:
                print(f"Error rendering attendace_download.html: {e}")  

        # Render the template with necessary data
        return render(request, 'attendances/attendace_download.html', context)
         
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('academics:student_dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
    
# ===== code for showing logged in teachers subjects ======

def subject_list_to_check_attendance_for_teachers(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
        teacher = request.user
        teacher_sem = teacher.sem
        print(teacher_sem)
        # Filter subjects based on the user's current semester
        if teacher_sem in ['even']:
            subjects = Subject.objects.filter(teacher_id=teacher, sem__in=['2', '4', '6'])
        elif teacher_sem in ['odd']:
            subjects = Subject.objects.filter(teacher_id=teacher, sem__in=['1', '3', '5'])
        
        print(subjects)
        
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

        context ={
            'teacher': teacher,
            'teacher_sem': teacher_sem,
            'subjects':subjects
        }
        
        return render(request,'attendances/teacher_check_attendance.html',context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('/student-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
  
# ===== code to return attendance data for teachers ======

def attendace_summary_teachers(request,subject_code):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
        subject_instance = get_object_or_404(Subject, subject_code=subject_code)

        if subject_instance.subject_type in ['normal lab', 'ai/ml lab']:
            is_lab = True
        else:
            is_lab = False

        if request.method == 'POST':
            print(subject_code)
            teacher = request.user
            teacher_sem = teacher.sem
            selected_date = request.POST.get('attendance_date')
            selected_period = request.POST.get('selected_period')

            # Fetch attendance data based on the selected date, period, and subject code
            attendance_records = AttendanceData.objects.filter(
                subject_code=subject_instance,
                attendance_date=selected_date,
                section=subject_instance.section,
                period=selected_period
            )

            present_students = attendance_records.filter(attendance_status='P')
            absent_students = attendance_records.filter(attendance_status='A')

            context ={
                    'teacher': teacher,
                    'teacher_sem': teacher_sem,
                    'data':True,
                    'is_lab':is_lab,
                    'subject_code':subject_code,
                    'present_students': present_students,
                    'absent_students': absent_students,
                    'total_present': present_students.count(),
                    'total_absent': absent_students.count(),
                    'total_students': attendance_records.count(),
                    
            
                }
            return render(request, 'attendances/attendance_summary_for_teacher.html',context)

        else:
            print(subject_code)
            teacher = request.user
            teacher_sem = teacher.sem
    
            context ={
                    'teacher': teacher,
                    'teacher_sem': teacher_sem,
                    'data':False,
                    'is_lab':is_lab,
                    'subject_code':subject_code,          
                }
            return render(request, 'attendances/attendance_summary_for_teacher.html',context)

    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('/student-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
    

# ===== code for showing logged in students subjects ======  need to delete no use

def subject_list_to_check_attendance_for_students(request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        student = request.user

        # Use a dictionary to map course codes to course names
        course_mapping = {
            'BCA': 'Bachelor of Computer Application',
            'BCOM': 'Bachelor of Commerce',
            'BBA': 'Bachelor of Business Administration'
        }
        
        # Get the course name based on the student's course code
        course_name = course_mapping.get(student.course_id, 'Unknown')


        subjects = Subject.objects.filter(sem = student.sem, year_id=student.year_id, )
        print(subjects)
        print('\n')

        theory_subject = subjects.filter(section=student.section_id)
        print(theory_subject)
        print('\n')

        if student.lab_batch_type != '0':
            lab_batch = student.lab_batch_type
            lab_subject = subjects.filter(lab_batch_type=lab_batch)
        else:
            try:
                lab_subject=subjects.filter(lab_batch_type='0',subject_type='normal lab')
            except:
                lab_subject = 'no_lab_subjects'



        if student.language_pref != '0':
            lang_subject = subjects.filter(subject_type=student.language_pref)
        else:
            lang_subject = 'no_language_subjects'



        context = {
            'student': request.user,
            'course_name':course_name,
            'theory_subject':theory_subject,
            'lab_subject':lab_subject,
            'lang_subject':lang_subject
        }

        return render(request, 'attendances/student_check_attendance.html', context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
            return redirect('/teacher-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')
    

# ===== code to return attendance data for students ======

def attendance_data_for_students (request):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        student =request.user
        # Use a dictionary to map course codes to course names
        course_mapping = {
            'BCA': 'Bachelor of Computer Application',
            'BCOM': 'Bachelor of Commerce',
            'BBA': 'Bachelor of Business Administration'
        }
        
        # Get the course name based on the student's course code
        course_name = course_mapping.get(student.course_id, 'Unknown')
        if request.method == 'POST':
            date = request.POST.get('attendance_date')
            print('\n',date)

            try:
                attendance_history = AttendanceData.objects.filter(registration_no = student.username, section = student.section_id, sem=student.sem, attendance_date=date).order_by('period')
                print(attendance_history)
            
        
                context = {
                    'student': student,
                    'course_name':course_name,
                    'data':True,
                    'attendance_history':attendance_history    
                }

                return render(request, 'attendances/student_check_attendance_summary.html',context)
                
            except AttendanceData.DoesNotExist:
                print("No Data Found!")
                context = {
                    'student': student,
                    'course_name': course_name,
                    'data': False
                }
                return render(request, 'attendances/student_check_attendance_summary.html', context)
        
        
        else:
            context = {
                'student': student,
                'course_name':course_name,
                        
            }

            return render(request, 'attendances/student_check_attendance_summary.html',context)

        return render(request, 'attendances/student_check_attendance_summary.html',context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
            return redirect('/teacher-dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('accounts:login')
    elif request.user.is_anonymous:
        return redirect('accounts:login')

