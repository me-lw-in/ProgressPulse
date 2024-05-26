from django.contrib import admin
from academics.models import *

# Register your models here.
admin.site.register(Year)
admin.site.register(Course)
# admin.site.register(Section)   #no use
admin.site.register(Subject)
# admin.site.register(TeacherSubject)