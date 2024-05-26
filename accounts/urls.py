from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view , name='login'),
    path('forgot-password/', forgot_password , name='forgot-password'),
    path('otp-verification/', otp_verifying , name='otp-verification'),
    path('reset-password/', change_password , name='reset-password'),
    path('upload/',upload , name='upload'),
    
   
    
]


#     path('', views.loginUser, name='login_page'),
#     path('home', views.home, name='after_login_go_home'),
#     path('logout', views.logoutUser, name='logout_and_go_to_login_page'),
#     # path('uploadCsv', views.uploadCsvFile, name='upload_csv_file'),
#     path('forgotPasswordPage', views.check_Username_Password_send_Otp, name='check data and send otp'),
#     path('otpVerificationPage/<str:username>/', views.verify_otp, name='verifying otp'),
#     path('passwordReset/<str:username>/', views.reset_password, name='password_reset'),