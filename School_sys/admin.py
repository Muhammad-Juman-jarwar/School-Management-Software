from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserModel(UserAdmin):
    list_display=['username','user_type']




admin.site.register(CustomUser,UserModel)
admin.site.register(S_Clas)
admin.site.register(Session_year)
admin.site.register(Student)
admin.site.register(Teachers) 
admin.site.register(Subject) 
admin.site.register(Teachers_Notification)
admin.site.register(Teachers_Leave)
admin.site.register(Student_Notification)
admin.site.register(Students_Leave)
admin.site.register(Time_Table)
admin.site.register(SetFee)
admin.site.register(Payment)
admin.site.register(Attendence)
admin.site.register(Attendence_Report)


