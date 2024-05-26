from django.shortcuts import render,get_object_or_404,redirect
from academics.models import Subject
from accounts.models import CustomUser

# Create your views here.

# =====get class details=====
def student_details(request,subject_code):
    if not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'teacher').exists():
        teacher = request.user
        subject = get_object_or_404(Subject, subject_code=subject_code)
    
        if subject.subject_name in ['kannada', 'hindi', 'malayalam']:
            if subject.section in ['A', 'B']:
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, language_pref=subject.subject_name, section_id=subject.section)
            else:
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, language_pref=subject.subject_name)
        else:
            if subject.subject_type == 'normal theory':
                if subject.section == '0':
                    students = CustomUser.objects.filter(year_id=subject.year_id.year_name)
                else:
                    students = CustomUser.objects.filter(year_id=subject.year_id.year_name, section_id=subject.section)
            elif subject.subject_type == 'aviation':
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, course_type='aviation')
            elif subject.subject_type == 'logistics':
                students = CustomUser.objects.filter(year_id=subject.year_id.year_name, course_type='logistics')
            elif subject.subject_type == 'normal lab':
                if subject.lab_batch_type == '0':
                    students = CustomUser.objects.filter(year_id=subject.year_id.year_name)
                if subject.lab_batch_type == 'normal':
                    students = CustomUser.objects.filter(lab_batch_type='normal',year_id=subject.year_id.year_name)
                if subject.lab_batch_type == 'addon':
                    students = CustomUser.objects.filter(lab_batch_type='addon',year_id=subject.year_id.year_name)
    
        context = {
            'teacher': teacher,
            'subject': subject,
            'students': students
        }
        print(context)
        return render(request, 'attendances/take_attendance.html', context)
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'student').exists():
        return redirect('academics:student_dashboard')
    elif not request.user.is_anonymous and CustomUser.objects.filter(username = request.user.username, user_type = 'admin').exists():
        return redirect('academics:student_dashboard')
    elif request.user.is_anonymous:
        return redirect('accounts:login')