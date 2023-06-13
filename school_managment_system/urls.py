"""school_managment_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import Teachers_views, views,HOD_views,Student_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('base/',views.BASE,name='base'),


    
    
    # login path
    path('',views.LOGIN,name='login'),
    path('dologin',views.doLogin,name='doLogin'),
    path('dologout',views.doLogout,name='doLogout'),

    #profile Update
    path('profile',views.Profile,name='profile'),
    path('profile/update',views.Profile_Update,name='profile_update'),



    # HOD PANEL URL

    # Students
    path('HOD/home',HOD_views.HOME,name='hod_home') ,
    path('HOD/student/add',HOD_views.Add_Student,name='Add_Student'),
    path('HOD/student/view',HOD_views.View_Student,name='View_Student'),
    path('HOD/student/edit/<str:id>',HOD_views.Edit_Student,name='Edit_student'),
    path('HOD/student/update<str:id>',HOD_views.Update_Student,name='Update_Student'),
    path('HOD/student/delete/<str:admin>',HOD_views.Delete_Student,name='delete_student'),

    # Teachers
     path('HOD/teacher/add',HOD_views.Add_Teacher,name='add_teacher'),
     path('HOD/teacher/view',HOD_views.View_Teacher,name='view_teachers'),
     path('HOD/teacher/edit/<str:id>',HOD_views.Edit_Teacher,name='edit_teacher'),
     path('HOD/teacher/update/<str:id>',HOD_views.Update_Teacher,name='update_teacher'),
     path('HOD/teacher/delete/<str:admin>',HOD_views.Delete_Teacher,name='delete_teacher'),


#   Class 
    path('HOD/class/add',HOD_views.Add_Class,name='add_class'),
    path('HOD/class/view',HOD_views.View_Class,name='view_class'),
    path('HOD/class/edit/<str:id>',HOD_views.Edit_Class,name='edit_class'),
    path('HOD/class/update/<str:id>',HOD_views.Update_Class,name='update_class'),
    path('HOD/class/delete/<str:id>',HOD_views.Delete_Class,name='delete_class'),
   
#   Subjects
    path('HOD/subject/add',HOD_views.Add_Subject,name='add_subject'),
    path('HOD/subject/view',HOD_views.View_Subject,name='view_subject'),
    path('HOD/subject/edit/<str:id>',HOD_views.Edit_Subject,name='edit_subject'),
    path('HOD/subject/update/<str:id>',HOD_views.Update_Subject,name='update_subject'),
    path('HOD/subject/delete/<str:id>',HOD_views.Delete_Subject,name='delete_subject'),

# SessionYear
    path('HOD/sessionyear/add',HOD_views.Add_Session,name='add_session'),
    path('HOD/sessionyear/view',HOD_views.View_Session, name="view_session"),
    path('HOD/sessionyear/edit/<str:id>',HOD_views.Edit_Session, name="edit_session"),
    path('HOD/sessionyear/update/<str:id>',HOD_views.Update_Session, name="update_session"),
    path('HOD/sessionyear/delete/<str:id>',HOD_views.Delete_Session, name="delete_session"),

#  TIME TABLE
path('HOD/add_time_table',HOD_views.Add_Time_Table,name='add_time_table'),
path('HOD/save_time_table',HOD_views.Save_Time_Table,name='save_time_table'),
path('HOD/view_time_table',HOD_views.view_time_table,name='view_time_table'),
path('HOD/generate_time_table',HOD_views.Generate_Time_Table,name='generated_time_table'),
path('HOD/edit_time_table',HOD_views.Edit_Time_Table,name='edit_time_table'),
path('HOD/show_time_table',HOD_views.Show_Time_Table,name='show_time_table'),
path('HOD/edit_time_table_data/<str:id>',HOD_views.Edit_Time_Table_Data,name='edit_time_table_data'),
path('HOD/update_time_table_data/<str:id>',HOD_views.Update_Time_Table_Data,name='update_time_table_data'),
path('HOD/delete_time_table_data/<str:id>',HOD_views.Delete_Time_Table_Data,name='delete_time_table_data'),


# Student Attendence
path('HOD/take_attendence',HOD_views.Take_Attendence,name='take_attendence'),
path('HOD/save_attendence',HOD_views.Save_Attendence,name='save_attendence'),
path('HOD/view_attendence',HOD_views.View_Attendence,name='view_attendence'),







# HOD TO Staff Notifications
    
    path('HOD/Teachers/send_notification',HOD_views.Teacher_Send_Notification,name='teacher_send_notification'),
    path('HOD/Teachers/save_notification',HOD_views.Save_Notification,name='save_notification'),
    path('HOD/Teacher/leave_view',HOD_views.View_Teacher_Leave, name="view_teacher_leave"),
    path('HOD/Teacher/approve_apply_leave/<str:status>',HOD_views.Approve_Teacher_Leave,name='approve_teacher_leave'),
    path('HOD/Teacher/disapprove_apply_leave/<str:status>',HOD_views.Disapprove_Teacher_Leave,name='disapprove_teacher_leave'),
   
#    HOD TO STUDENT NOTIFICATION
    path('HOD/Student/send_notification',HOD_views.Student_Send_Notification,name='student_send_notification'),
    path('HOD/Student/save_notification',HOD_views.Student_Save_Notification,name='student_save_notification'),
    
    path('HOD/Student/view_student_leave',HOD_views.View_Student_Leave,name='view_student_leave'),
    path('HOD/Student/approve_student_leave/<str:id>',HOD_views.Approve_Student_Leave,name='approve_student_leave'),
    path('HOD/Student/disapprove_student_leave/<str:id>',HOD_views.Disapprove_Student_Leave,name='disapprove_student_leave'),

#  Fee Management
    path('HOD/Fee/set_fee',HOD_views.Set_Fee,name='set_fee'),
    path('HOD/Fee/add_fee',HOD_views.Add_Fee,name='add_fee'),
    path('HOD/Fee/view_fee',HOD_views.View_Fee,name='view_fee'),
    path('HOD/Fee/show_fee',HOD_views.Show_Fee,name='show_fee'),
    path('HOD/Fee/edit_fee/<str:id>',HOD_views.Edit_Fee,name='edit_fee'),
    path('HOD/Fee/update_fee/<str:id>',HOD_views.Update_Fee,name='update_fee'),
    path('HOD/Fee/delete_fee/<str:id>',HOD_views.Delete_Fee,name='delete_fee'),
    path('HOD/Fee/show_students_fee',HOD_views.Show_Studets_Fee,name='show_students_fee'),
    path('HOD/Fee/get_fee',HOD_views.Get_Fee,name='get_fee'),





# --------------------------------------------------------------#
    # '''    Staff Panel Urls        '''
    path('Teacher/Home',Teachers_views.Home,name='teacher_home'),
    path('Teacher/Notification',Teachers_views.Notifications,name='notifications'),
    path('Teacher/mark_as_done/<str:status>',Teachers_views.Mark_As_Done,name="mark_as_done"),
    path('Teacher/apply_leave',Teachers_views.Tecaher_Apply_Leave, name='teacher_apply_leave'),
    path('Teacher/apply_leave_save',Teachers_views.Teacher_Apply_Leave_Save,name='teacher_apply_leave_save'),
    
    # teacher Time Table panel
    path('Teacher/show_teacher_time_table',Teachers_views.Show_Teacher_Time_Table,name='show_teacher_time_table'),


    # STUDENT PANEL URLS
    path('Student/home',Student_views.Home,name='student_home'),
    path('Student/view_notification',Student_views.View_Notification,name='view_notifications'),
    path('Student/mark_as_read/<str:status>',Student_views.Mark_As_Read,name='mark_as_read'),
    path('Student/student_apply_leave',Student_views.Student_Apply_Leave,name='student_apply_leave'),
    path('Student/student_save_leave',Student_views.Student_Save_Leave,name='student_save_leave'),

    # Student Time_Table

    path('Student/show_student_time_table',Student_views.Show_Student_Time_Table,name='show_student_time_table'),







# Export








] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
