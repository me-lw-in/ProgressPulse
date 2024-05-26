import csv
import random 
from django.core.cache import cache
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
# from accounts.models import Attendance
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User_Data



# Create your views here.

# =======user authenitcation======

def login_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        try:
            is_a_user = User_Data.objects.filter(user_id = username, user_type = user_type).exists()
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None and is_a_user:
                login(request, user)
                if user_type == 'student':
                    return redirect('academics:student_dashboard')
                elif user_type == 'teacher':
                    return redirect('academics:teacher_dashboard')    
            else:
                error_message = 'Invalid username or password'
                return render(request, 'accounts/login.html', {'error_message': error_message})
        except User.DoesNotExist:
            error_message = 'Invalid username or user type'
            return render(request, 'accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')


# =========forgot-password=======

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User_Data.objects.get(user_id = username, email = email)
            request.session['user_email'] = user.email
            request.session['user_id'] = user.user_id
            
            otp = str(random.randint(111111, 999999))
            print(otp)
            cache_key = f'otp_{user.email}'
            cache.set(cache_key, otp, timeout=600)  # OTP expires in 10 minutes
            subject = "OTP for password reset"
            message = f"Your OTP is: {otp}\n\nPlease note that this OTP will expire in 10 minutes."
            from_email = settings.EMAIL_HOST_USER
            recipient_email = [user.email]
            send_mail(subject,message,from_email,recipient_email)
            # message = "Otp Sent Successfully!"
            return redirect('accounts:otp-verification')
        except User_Data.DoesNotExist:
            error_message = "Wrong username or email!"
            return render(request, 'accounts/forgot_password.html', {'message': error_message})   
    return render(request, 'accounts/forgot_password.html')

# ======otp verifying=========

def otp_verifying(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('user_email')
        username = request.session.get('user_id')
        print(username)
        print(email)
        cache_key =  f'otp_{email}'
        stored_otp = cache.get(cache_key)
        if stored_otp is not None:
            if entered_otp == stored_otp:
                
                return render(request, 'accounts/otp_and_password_reset.html', {'success': True})
            else:
                error_message = "Incorrect otp. Please try again!"
                return render(request, 'accounts/otp_and_password_reset.html', {'success': False, 'error_message':error_message})
        else:
            # error_message = "Otp expired!"
            return render(request, 'accounts:forgot-password')
    else:
        return render(request, 'accounts/otp_and_password_reset.html')
    

# =======password reset======

# def reset_password(request,username):
#     return HttpResponse("hello")


def reset_password_1(request):
    print("hello")
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        username = request.session.get('user_id')
        try:
            user = User.objects.get(username = username)
            if password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                cache.clear()
                request.session.flush()
                return redirect('accounts:login')
            else:
                error_message = "Password do not match. Please try again"
                return render(request, 'accounts/otp_and_password_reset.html', {'error_message':error_message ,'success':True} )
        
        except User.DoesNotExist:
            error_message = "User not found."
            return render(request, 'accounts/otp_and_password_reset.html', {'error_message': error_message, 'success': True})
    else:
        return redirect('accounts:forgot-password')

        
        

        
























# ==================home===================

def home(request):
    if request.user.is_anonymous:
        return redirect('accounts/login.html')
    return render(request,'home.html')


# ==============check login credentials==============

def loginUser(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        #check user has entered correct credentials
        user = authenticate(username=username, password=password)
        
        # checks if user added credentials or not
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect("/home")
        else:
            return render(request, "login.html")
            

    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

# ================attendance csvfile upload======================= 
#============== dont need it for right now============


# def uploadCsvFile(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         decoded_file = csv_file.read().decode('utf-8').splitlines()
#         reader = csv.DictReader(decoded_file)
#         for row in reader:
#                 attendance = Attendance(
#                     registration_no=row['Registration No'],
#                     section_id=row['Section ID'],
#                     subject_id=row['Subject ID'],
#                     date=row['Date'],
#                     period=int(row['Period']),  # Convert to integer
#                     status=row['Status'],
#                     course_id=row['Course ID']
#                 )
#                 attendance.save()
#         return HttpResponse("Succesfull!")
#     return render(request, 'upload_csv.html')

# ==============check username and email matches with the database=================

def check_Username_Password_send_Otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get( 'email' )
        try:
            # checking if user is found or not 
            user = User.objects.get(username=username , email =email)
            print(user)
             # Generate OTP
            otp = str(random.randint(111111, 999999))
            print(otp)
            cache_key = f'otp_{email}'
            print(cache_key)
            cache.set(cache_key, otp, timeout=600)  # OTP expires in 10 minutes
            subject = "OTP for password reset"
            message = f"Your OTP is: {otp}\n\nPlease note that this OTP will expire in 10 minutes."
            from_email = settings.EMAIL_HOST_USER
            recipient_email = [email]
            send_mail(subject,message,from_email,recipient_email)
            

            return redirect("verifying otp", username=username)
        
        except User.DoesNotExist: 
             error_message = 'Invalid username or email.'
             return render(request, 'forgot_password.html', {'error_message': error_message})

    return render(request, 'forgot_password.html')

# ==============check if the otp matches with the genrated otp ===================

def verify_otp(request,username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username = username)
            user_entered_otp = request.POST.get( 'otp' )
            cache_key =  f'otp_{user.email}'
            stored_otp = cache.get(cache_key)
            print(user_entered_otp)

            if stored_otp is not None:
                if user_entered_otp == stored_otp:
                    cache.delete(cache_key)
                    return redirect("password_reset.html",username= username)
                else:
                    error_message = 'Invalid OTP. Please try again.'
                    return render(request ,'verifying otp',{'error_message':error_message , 'username':username} )
            else:
                error_message = 'OTP has expired. Please request a new OTP.'
                return render(request ,'check data and send otp',{'error_message':error_message} )

        except User.DoesNotExist:
            error_message = 'User does not exist.'
        return render(request, 'verifying otp',{'error_message': error_message ,'username': username})

    return render(request, 'otp_verification.html', {'username': username})

# ============reseting the password =============

def reset_password(request,username):
    if request.method == 'POST':
        changed_password = request.POST.get('password')
        confirm_changed_password = request.POST.get('confirmPassword')
        try:
            if changed_password == confirm_changed_password:
                user =User.objects.get(username = username)
                user.set_password(changed_password)
                user.save()
                return redirect('login_page')
            else:
                error_message = "Password do not Match!"
                return render(request, 'password_reset',{'error_message':error_message , 'username':username })
        except User.DoesNotExist:
            error_message = "User does not exist!"
            return render(request, 'check data and send otp' , {'error_message':error_message})
        except Exception as e:
            error_message = "An error occurred during password reset. Please try again."
            return render(request , 'password_reset', {'error_message':error_message , 'username':username })
              
    return render (request,'password_reset')