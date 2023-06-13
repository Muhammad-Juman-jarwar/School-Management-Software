from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from School_sys.models import Time_Table,S_Clas,Payment, Session_year, CustomUser ,Student,Teachers,Subject,Teachers_Notification,Teachers_Leave,Student_Notification,Students_Leave,SetFee,Attendence,Attendence_Report
from django.contrib import messages
from .tables import TimeTableTable
from datetime import datetime ,date
from django.db import IntegrityError

import pytz
import math

tz = pytz.timezone('Asia/Karachi')

# get the current date and time in Pakistan
now = datetime.now(tz)
formated_date = now.strftime("%Y-%m-%d %H:%M:%S")



@login_required(login_url='/')
def HOME(request):

    student_count= Student.objects.all().count()
    Teacher_count= Teachers.objects.all().count()
    Class_count=S_Clas.objects.all().count()
    subject_count= Subject.objects.all().count()

    student_Male=Student.objects.filter(Gender='Male').count()
    student_female=Student.objects.filter(Gender='Female').count()
    student_others=Student.objects.filter(Gender='Others').count()




    context={
        'Student_count':student_count,
        'Teacher_count':Teacher_count,
        'Class_count':Class_count,
        'Subject_count':subject_count,
        'Smale':student_Male,
        'Sfemale':student_female,
        'Sothers':student_others,
    }
    return render(request,'HOD/home.html',context)


@login_required(login_url='/')
def Add_Student(request):
    try:

        Class= S_Clas.objects.all()
        session_year =Session_year.objects.all()
        global formated_date

        

        if request.method=="POST":
            profile_pic=request.FILES.get("profile_pic")
            first_name=request.POST.get("first_name")
            last_name=request.POST.get("last_name")
            email=request.POST.get("email")
            user_name=request.POST.get("user_name")
            password=request.POST.get("password")
            address=request.POST.get("address")
            gender=request.POST.get("gender")
            father_name=request.POST.get("f_name")
            dob=request.POST.get("dob")
            S_class_id=request.POST.get("S_class_id")
            session_year_id=request.POST.get("session_year_id")

            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request,"email is already taken")
                return redirect('Add_Student')

            if CustomUser.objects.filter(username=user_name).exists():
                messages.warning(request,"username is already taken")
                return redirect('Add_Student')
            else:
                user= CustomUser(
                    first_name=first_name,
                    last_name=last_name,
                    username=user_name,
                    email=email,
                    profile_pic=profile_pic,
                    user_type=3)
                
                user.set_password(password)
                user.save()
                

                S_class=S_Clas.objects.get(id=S_class_id)
                session_year=Session_year.objects.get(id=session_year_id)
                student = Student(admin=user,Gender=gender,Father_Name=father_name,DOB=dob,address=address,Session_year_id=session_year,S_Class_id=S_class,created_at=formated_date )
                student.save()
                messages.success(request,user.first_name+' '+ user.last_name +" succesfully added")
                return redirect('Add_Student')

        context={
            'class':Class,
            'session_year':session_year
            }


        return render(request,'HOD/add_student.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('hod_home')


@login_required(login_url='/')
def View_Student(request):
    student= Student.objects.all()
    context={
        'student':student
    }
    return render(request,'HOD/view_student.html',context)


@login_required(login_url='/')
def Edit_Student(request,id):
    student = Student.objects.filter(id=id)
    session_year=Session_year.objects.all()
    Class= S_Clas.objects.all()


    context={
        'student':student,
        'class':Class,
        'session_year':session_year,
    }
    return render(request,'HOD/update.html',context)


def Update_Student(request,id):
    
    
    if request.method=="POST":
       
        # student_id=request.POST.get("student_id")
        profile_pic=request.FILES.get("profile_pic")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        user_name=request.POST.get("user_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        gender=request.POST.get("gender")
        father_name=request.POST.get("f_name")
        dob=request.POST.get("dob")
        S_class_id=request.POST.get("S_class_id")
        session_year_id=request.POST.get("session_year_id")

        # CustomUserModel Updation
        users = CustomUser.objects.get(id=id)
        users.first_name=first_name
        users.last_name=last_name
        users.email=email
        users.username=user_name
        if password!=None and password!="":
            users.set_password(password)
        if profile_pic!=None and profile_pic!="":
            users.profile_pic=profile_pic
        users.save()
        
        
        # StudentModel Updation 
        
        global formated_date

        student= Student.objects.get(admin=id)
        
        if dob!=None and dob!="":
            student.DOB=dob
        student.address=address
        student.Gender=gender
        student.Father_Name=father_name
        student.updated_at= formated_date

        # CourseUpdation for Student
        Sclass=S_Clas.objects.get(id=S_class_id)
        student.S_Class_id=Sclass

        # SessionYearUpdation for student
        SessionYear=Session_year.objects.get(id=session_year_id)
        Student.Session_year_id=SessionYear

        student.save()
        messages.success(request,'Record Updated Successfully')
        return redirect('View_Student')


    
    
    return render(request,'HOD/update.html')


@login_required(login_url='/')
def Delete_Student(request,admin):
    try:
        student=CustomUser.objects.get(id=admin)
        student.delete()
        messages.success(request,"Record Deleted successfully")
        return redirect('View_Student')
    except Exception as e:
        messages.error(request,e)
        return redirect('View_Student')



@login_required(login_url='/')
def Add_Class(request):
    
    if request.method == "POST":
        class_name=request.POST.get("Class_name")
        Cname= class_name.upper()
        global formated_date
        print(formated_date)

    
        if S_Clas.objects.filter(name=Cname).exists():
            messages.error(request,"Class Already Exist")
            return redirect('add_class')
        else:
            sclass=S_Clas(
                name=Cname,
                created_at=formated_date
            )
            sclass.save()
            messages.success(request,"Class Added Successfully")

            

    return render(request,'HOD/add_class.html')



@login_required(login_url='/')
def View_Class(request):
    S_class= S_Clas.objects.all()
    context={
        'S_class':S_class
    }
    return render(request,'HOD/view_class.html',context)





@login_required(login_url='/')
def Edit_Class(request,id):
    S_class=S_Clas.objects.get(id=id)
    context ={
        'S_class':S_class
    }
    return render(request,'HOD/edit_class.html',context)




@login_required(login_url='/')
def Update_Class(request,id):
    try:
        if request.method == "POST":
            global formated_date
            S_Class=S_Clas.objects.get(id=id)
            Class_name=request.POST.get("Class_name")
            S_Class.name=Class_name
            S_Class.updated_at=formated_date
            S_Class.save()
            messages.success(request,'Updated Successfully')
            return redirect('view_class')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_class')



@login_required(login_url='/')
def Delete_Class(request,id):
    try:
        S_class=S_Clas.objects.get(id=id)
        S_class.delete()
        messages.success(request,"Record Deleted successfully")
        return redirect('view_class')
    except Exception as  e:
        messages.error(request,e)
        return redirect('view_class')
    

@login_required(login_url='/')
def Add_Teacher(request):
    try:
        if request.method == "POST":
            profile_pic=request.FILES.get("profile_pic")
            first_name=request.POST.get("first_name")
            last_name=request.POST.get("last_name")
            email=request.POST.get("email")
            user_name=request.POST.get("user_name")
            password=request.POST.get("password")
            address=request.POST.get("address")
            gender=request.POST.get("gender")
            father_name=request.POST.get("f_name")
            contact = request.POST.get("phone")
            global formated_date


           
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request,'email already exists')
                return redirect('add_teacher')
            if CustomUser.objects.filter(username=user_name).exists():
                messages.warning(request,'username already exists')
                return redirect('add_teacher')
            if Teachers.objects.filter(contact=contact):
                messages.warning(request,'Contact No already exists')
                return redirect('add_teacher')

            
            else:
                user= CustomUser(first_name=first_name,last_name=last_name,email=email,username=user_name,profile_pic=profile_pic,user_type=2)
                user.set_password(password)
                user.save()
                Teacher=Teachers(
                    admin=user,
                    address=address,
                    gender=gender,
                    Father_Name=father_name,
                    contact=contact,
                    created_at=formated_date,
                    updated_at=formated_date
                )
                Teacher.save()
                messages.success(request,'Teacher Added Successfully')
                return redirect('view_teachers')
        return render(request,'HOD/add_teacher.html')



            
    except Exception as e:
        messages.error(request,e)
        return redirect('add_teacher')

@login_required(login_url='/')
def View_Teacher(request):
    try:
     Teacher=Teachers.objects.all()
     context={
         'Teacher':Teacher
     }

     return render(request,'HOD/view_teachers.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('hod_home')



@login_required(login_url='/')
def Edit_Teacher(request,id):
    try:
            Teacher=Teachers.objects.get(id=id)
            context={
                'Teacher':Teacher
                }
            return render(request,'HOD/edit_teacher.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('view_teachers')

@login_required(login_url='/')
def Update_Teacher(request,id):
    try:
        if request.method == "POST":
            global formated_date
            profile_pic=request.FILES.get("profile_pic")
            first_name=request.POST.get("first_name")
            last_name=request.POST.get("last_name")
            email=request.POST.get("email")
            user_name=request.POST.get("user_name")
            password=request.POST.get("password")
            address=request.POST.get("address")
            gender=request.POST.get("gender")
            father_name=request.POST.get("f_name")
            contact=request.POST.get('phone')

             # CustomUserModel Updation
            users = CustomUser.objects.get(id=id)
            users.first_name=first_name
            users.last_name=last_name
            users.email=email
            users.username=user_name
            global formated_date

            if password!=None and password!="":
                users.set_password(password)
            if profile_pic!=None and profile_pic!="":
                users.profile_pic=profile_pic
            users.save()

            # Teacher Model Updation
            Teacher=Teachers.objects.get(admin=id)

            Teacher.address=address
            Teacher.contact=contact
            Teacher.Father_Name=father_name
            Teacher.gender=gender
            Teacher.updated_at=formated_date
            Teacher.save()
            messages.success(request,'Updated Successfully')
            return redirect('view_teachers')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_class')


@login_required(login_url='/')
def Delete_Teacher(request,admin):
    try:
        Users=CustomUser.objects.get(id=admin)
        Users.delete()
        messages.success(request,"Record Deleted successfully")
        return redirect('view_teachers')
    except Exception as  e:
        messages.error(request,e)
        return redirect('view_teachers')

@login_required(login_url='/')
def Add_Subject(request):
    try:
        global formated_date

        if request.method == "POST":
            Subject_Name= request.POST.get("subject_name")
         

           
            
            
        
            if Subject.objects.filter(name=Subject_Name).exists():
                    messages.warning(request,'This Subject is already Exist')
                    return redirect('add_subject')


                
            else:

             Subjects=Subject(
                name = Subject_Name,
                created_at=formated_date,
                updated_at=formated_date,
                )
             Subjects.save()
             messages.success(request,"Subject Added Successfully")
             return redirect('view_subject')








      

        return render(request,'HOD/add_subject.html')
    except Exception as e:
        messages.error(request,e)
        return redirect('hod_home')

@login_required(login_url='/')
def View_Subject(request):

    try:
        subject= Subject.objects.all()

        context={
            'Subject':subject,
        }

        return render(request,'HOD/view_subject.html',context)
    except Exception as e:
         messages.error(request,e)
         return redirect('hod_home')


@login_required(login_url='/')
def Edit_Subject(request,id):
    try:
        Subject_id=Subject.objects.get(id=id)
        context={
            'Subject_id':Subject_id
        }


        return render(request,'HOD/edit_subject.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('view_subject')

@login_required(login_url='/')
def Update_Subject(request,id):
    try:
        if request.method=="POST":

            subject_name=request.POST.get("subject_name")
        
            Subject_id=Subject.objects.get(id=id)
            if Subject.objects.filter(name=subject_name).exists() :
                    messages.warning(request,'This Subject is already exists')
                    return redirect('add_subject')
            else:
            
                Subject_id.name=subject_name
                Subject_id.updated_at=formated_date
                Subject_id.save()
                messages.success(request,"Class Updated Successfully")
                return redirect('view_subject')
        
    except Exception as e:
        messages.error(request,e)
        return redirect('edit_subject')

@login_required(login_url='/')
def Delete_Subject(request,id):
    try:
        Subject_id=Subject.objects.get(id=id)
        Subject_id.delete()
        messages.success(request,'Class Deleted Successfully')
        return redirect('view_subject')
    except Exception as e:
        messages.success(request,'Class Deleted Successfully')
        return redirect('view_subject')


@login_required(login_url='/')
def Add_Session(request):

    try:
     if request.method == "POST":
         
         start=request.POST.get("session_start")
         end=request.POST.get("session_end")
         session_start =datetime.strptime(start, '%Y-%m-%d').date()
         session_end = datetime.strptime(end, '%Y-%m-%d').date()
        #  s_s=session_start.strftime("%m/%d/%Y")
        #  s_e=session_end.strftime("%m/%d/%Y")



         if session_start>=session_end:
             messages.warning(request," Invalid Session Choice")
             return render(request,'HOD/add_session_year.html')
         if Session_year.objects.filter(Session_start=start).exists() and Session_year.objects.filter(Session_end=end).exists():
              messages.warning(request,"  Session Already Exist")
              return render(request,'HOD/add_session_year.html')
         else:
            session= Session_year(
                Session_start=start,
                Session_end=end,
                   )
            session.save()
            messages.success(request,"Session Added Successfully")
            return render(request,'HOD/add_session_year.html')

             


     return render(request,'HOD/add_session_year.html')
    except Exception as e:
     messages.error(request,e)
     return redirect('hod_home')

@login_required(login_url='/')
def View_Session(request):
    try:
        session=Session_year.objects.all()
        context={
            'Session':session
        }
        return render(request,"HOD/view_session_year.html",context)
    except Exception as e:
        messages.error(request,e)
        return redirect('hod_home')
    


@login_required(login_url='/')
def Edit_Session(request,id):
    try:
        session=Session_year.objects.filter(id=id)
        
        context={
            'session':session,
            'session_id':id,
        }
        
        return render(request,'HOD/edit_session.html',context)
    
    except Exception as e:
        messages.error(request,e)
        return redirect('view_session')

@login_required(login_url='/')
def Update_Session(request,id):
    try:
        if request.method == "POST":
            session=Session_year.objects.get(id=id)
            start=request.POST.get("session_start")
            end=request.POST.get("session_end")
            session_start =datetime.strptime(start, '%Y-%m-%d').date()
            session_end = datetime.strptime(end, '%Y-%m-%d').date()
            if session_start>=session_end:
                messages.warning(request," Invalid Session Choice")
                return redirect('edit_session')
            else:
                session.Session_start=start
                session.Session_end=end
                session.save()
                messages.success(request," Session Updated Successfully")
                return redirect('view_session')
            
    except Exception as e:
         messages.error(request,e)
         return redirect('view_session')

@login_required(login_url='/')
def Delete_Session(request,id):
    try:
        session=Session_year.objects.get(id=id)
        session.delete()
        messages.success(request,'Session Deleted Successfully')
        return redirect('view_session')



    except Exception as e:
        messages.error(request,e)
        return redirect('view_session')


@login_required(login_url='/')
def Teacher_Send_Notification(request):
     
     Teacher=Teachers.objects.all()
     message=Teachers_Notification.objects.all().order_by('-id')[0:5]
     context={
         'Teacher':Teacher,
         'messag':message,
     }
     return render(request,'HOD/Send_teacher_notification.html',context)



@login_required(login_url='/')
def Save_Notification(request):
    try:
        if request.method =="POST":
            Teacher_Id= request.POST.get('Teacher_id')

            

            message= request.POST.get('mess')
            All= request.POST.get('All')
            if All == "All":
                
                 teacher_ids = Teachers.objects.values_list('id', flat=True)
        
                 notifications=[]
                 for teacher_id in teacher_ids:
                     
                     
                     
                     teacher = Teachers.objects.get(id=teacher_id)
                  
                     notification=Teachers_Notification(
                     teacher_id=teacher,
                     message=message,   )
                     notifications.append(notification)
                 Teachers_Notification.objects.bulk_create(notifications)  
                 messages.success(request,'Message Successfully Sent To All')
                 return redirect('teacher_send_notification')
            else:
                teacher=Teachers.objects.get(admin=Teacher_Id)
                notification=Teachers_Notification(
                teacher_id=teacher,
                message=message,
                )
                notification.save()
        
                messages.success(request,'Message Successfully Sent')
                return redirect('teacher_send_notification')
        
        
    


    
    
    except Exception as e:
        messages.error(request,e)
        return redirect('teacher_send_notification')


        
@login_required(login_url='/')
def View_Teacher_Leave(request):

    Leave_data=Teachers_Leave.objects.all()
    context={
        'leave_date':Leave_data,
    }
    return render(request,'HOD/View_teacher_leave.html',context)


@login_required(login_url='/')
def Approve_Teacher_Leave(request,status):
    try:
            teacher=Teachers.objects.get(admin=status)
            status=Teachers_Leave.objects.get(Teacher_id=teacher)
            status.status=1
            status.save()
    
            return redirect('view_teacher_leave')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_teacher_leave')
    
@login_required(login_url='/')
def Disapprove_Teacher_Leave(request,status):
    try:
            teacher=Teachers.objects.get(admin=status)
            status=Teachers_Leave.objects.get(Teacher_id=teacher)
            status.status=2
            status.save()
    
           
            return redirect('view_teacher_leave')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_teacher_leave')

@login_required(login_url='/')
def Student_Send_Notification(request):
     
     Class=S_Clas.objects.all()
     Session=Session_year.objects.all()
     message=Student_Notification.objects.all().order_by('-id')[0:5]
     context={
         'SClass':Class,
         'messag':message,
         'Session':Session,
     }
     return render(request,'HOD/student_send_notification.html',context)

@login_required(login_url='/')
def Student_Save_Notification(request):
    try:
        if request.method=="POST":
           
            All= request.POST.get('All')
            if All == "All":
                 message=request.POST.get('Notification_message')
                
                 class_ids = S_Clas.objects.all()
                 session_ids = Session_year.objects.all()

        
                 notifications=[]

                 for C_id in class_ids :
                     
                     
                     for ses_id in session_ids: 
                    #  Class = S_Clas.objects.get(id=C_id.id)
                    #  session=Session_year.objects.get(id=ses_id.id)
                    #  print(Class)
                        notification=Student_Notification(
                        Class=C_id,
                        session=ses_id,
                        message=message,   )
                        notifications.append(notification)
                 Student_Notification.objects.bulk_create(notifications)  
                 messages.success(request,'Message Successfully Sent To All')
                 return redirect('student_send_notification')
            else:
                Class_id=request.POST.get('S_class_id')
                session_id=request.POST.get('session_year_id')
                message=request.POST.get('Notification_message')
                get_class=S_Clas.objects.get(id=Class_id)
                get_session=Session_year.objects.get(id=session_id)
                notification=Student_Notification(
                Class=get_class,
                session=get_session,
                message=message,
                    )
                notification.save()
                messages.success(request,'Notification sent Successfully')
                return redirect('student_send_notification')
    
    

    except Exception as e:
          messages.error(request,e)
          return redirect('student_send_notification')
    


@login_required(login_url='/')
def Approve_Student_Leave(request,id):
    try:
            # student=Student.objects.get(admin=status)
            status=Students_Leave.objects.get(id=id)
            status.status=1
            status.save()
            return redirect('view_student_leave')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_student_leave')
    
@login_required(login_url='/')
def Disapprove_Student_Leave(request,id):
    try:
            # student=Student.objects.get(admin=status)
            status=Students_Leave.objects.get(id=id)
            status.status=2
            status.save()           
            return redirect('view_student_leave')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_student_leave')
    



@login_required(login_url='/')
def View_Student_Leave(request):


    Leave_data=Students_Leave.objects.all()
    context={
        'leave_date':Leave_data,
    }
    return render(request,'HOD/view_student_leave.html',context)


@login_required(login_url='/')
def Add_Time_Table(request):

    subject=Subject.objects.all()
    Class=S_Clas.objects.all()
    Session=Session_year.objects.all()
    teacher=Teachers.objects.all()
    day=Time_Table.DAY_CHOICES
    context={
        'subject':subject,
        'Class':Class,
        'Session':Session,
        'teacher':teacher,
        'day':day,

    }

    return render(request,'HOD/add_time_table.html',context)


@login_required(login_url='/')
def Save_Time_Table(request):

    try:
        if request.method=="POST":
            subject_id = request.POST.get('subject_id')
            teacher_id = request.POST.get('teacher_id')
            class_id = request.POST.get('S_class_id')
            session_year_id = request.POST.get('Session_id')
            day = request.POST.get('day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            if subject_id=="select_subject" or teacher_id=="select_teacher" or class_id=="selec_class" or session_year_id=="select_session" or day=="selec_session":
                messages.warning(request,'please select all field')
                return redirect('add_time_table')
            if start_time>=end_time:
                messages.warning(request,'please choose right time')
                return redirect('add_time_table')
            
            else:

                subjects=Subject.objects.get(id=subject_id)
                Class=S_Clas.objects.get(id=class_id)
                Session=Session_year.objects.get(id=session_year_id)
                teacher=Teachers.objects.get(id=teacher_id)
                if Time_Table.objects.filter(subject=subjects).exists() and Time_Table.objects.filter(CLass=Class).exists() and Time_Table.objects.filter(Session_year_id=Session).exists() and Time_Table.objects.filter(Teacher_id=teacher).exists() and Time_Table.objects.filter(day=day).exists() and Time_Table.objects.filter(start_time=start_time).exists() and Time_Table.objects.filter(end_time=end_time).exists():
                     messages.warning(request,'Time Table Already Exists')
                     return redirect('add_time_table')
                if Time_Table.objects.filter(Teacher_id=teacher).exists() and Time_Table.objects.filter(day=day).exists() and Time_Table.objects.filter(start_time=start_time).exists() and Time_Table.objects.filter(end_time=end_time).exists() and Time_Table.objects.filter(CLass=Class).exists():
                     messages.warning(request,'Selected Timing is Already Assigned to Teacher')
                     return redirect('add_time_table')
                else:
                        timetable=Time_Table(
                        subject=subjects,
                        Teacher_id=teacher,
                        CLass=Class,
                        Session_year_id=Session,
                        day=day,
                        start_time=start_time,
                        end_time=end_time,
                        created_at=formated_date
                                            )
                        timetable.save()
                        messages.success(request,'Time Table Added Successfully')
                        return redirect('add_time_table')
    except Exception as e:
        messages.error(request,e)
        return redirect('add_time_table')

@login_required(login_url='/')
def view_time_table(request):
    session=Session_year.objects.all()
    Class=S_Clas.objects.all()
    context={
        'session':session,
        'Class':Class,
    }
    return render(request,'HOD/view_time_table.html',context)


@login_required(login_url='/')
def Generate_Time_Table(request):
    try:
        if request.method=='POST':
            class_id=request.POST.get('S_class_id')
            session_id=request.POST.get('Session_id')
            time_table_data = Time_Table.objects.filter(CLass=class_id, Session_year_id=session_id)
            table= TimeTableTable(time_table_data)
        return render(request, 'HOD/generated_time_table.html',{'table':table})
    except Exception as e:
        messages.error(request,e)
        return redirect('hod_home')




@login_required(login_url='/')
def Edit_Time_Table(request):
    session=Session_year.objects.all()
    Class=S_Clas.objects.all()
    context={
        'session':session,
        'Class':Class,
    }
    return render(request,'HOD/edit_time_table.html',context)

@login_required(login_url='/')
def Show_Time_Table(request):
    try:
        if request.method=='POST':
            class_id=request.POST.get('S_class_id')
            session_id=request.POST.get('Session_id')
            time_table_data = Time_Table.objects.filter(CLass=class_id, Session_year_id=session_id)
            context={
                'Time_Table':time_table_data,
            }
            return render(request,'HOD/show_time_table_data.html',context)
    except Exception as e:
         messages.error(request,e)
         return redirect('hod_home')


@login_required(login_url='/')
def Edit_Time_Table_Data(request,id):
    time_table=Time_Table.objects.get(id=id)
    session=Session_year.objects.all()
    Class=S_Clas.objects.all()
    subject=Subject.objects.all()
    teacher=Teachers.objects.all()
    day=Time_Table.DAY_CHOICES
    context={
        'Table_data':time_table,
        'subject':subject,
        'Class':Class,
        'Session':session,
        'teacher':teacher,
        'day':day,
        'id':id,

    }

    return render(request,'HOD/Update_Time_Table.html',context)



@login_required(login_url='/')
def Update_Time_Table_Data(request,id):

    try:
        if request.method=="POST":
           
            subject_id = request.POST.get('subject_id')
            print(subject_id)
            teacher_id = request.POST.get('teacher_id')
            class_id = request.POST.get('S_class_id')
            session_year_id = request.POST.get('Session_id')
            day = request.POST.get('day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            table_data=Time_Table.objects.get(id=id)
            row_id = table_data.id


          
            if start_time>=end_time:
                messages.warning(request,'please choose right time')
                return redirect('edit_time_table_data')
            
            else:
                subjects=Subject.objects.get(id=subject_id)
                Class=S_Clas.objects.get(id=class_id)
                Session=Session_year.objects.get(id=session_year_id)
                teacher=Teachers.objects.get(id=teacher_id)
                # if Time_Table.objects.filter(subject=subjects).exists() and Time_Table.objects.filter(CLass=Class).exists() and Time_Table.objects.filter(Session_year_id=Session).exists() and Time_Table.objects.filter(Teacher_id=teacher).exists() and Time_Table.objects.filter(day=day).exists() and Time_Table.objects.filter(start_time=start_time).exists() and Time_Table.objects.filter(end_time=end_time).exists():
                #      messages.warning(request,'Time Table Already Exists')
                #      return redirect('edit_time_table')
                if Time_Table.objects.filter(Teacher_id=teacher).exclude(pk=row_id).exists() and Time_Table.objects.filter(day=day).exclude(pk=row_id).exists() and Time_Table.objects.filter(start_time=start_time).exclude(pk=row_id).exists()  and  Time_Table.objects.filter(end_time=end_time).exclude(pk=row_id).exists() and Time_Table.objects.filter(CLass=Class).exclude(pk=row_id).exists() and Time_Table.objects.filter(subject=subjects).exclude(pk=row_id).exists() and Time_Table.objects.filter(Session_year_id=session_year_id).exclude(pk=row_id).exists()  :
                     messages.warning(request,f"Can't Update! Timing is Already Assigned to Teacher")
                     return redirect('edit_time_table')
    

                else:
                
                    table_data.subject=subjects
                    table_data.Teacher_id=teacher
                    table_data.CLass=Class
                    table_data.Session_year_id=Session
                    table_data.day=day
                    table_data.start_time=start_time
                    table_data.end_time=end_time
                    table_data.updated_at
                                            
                    table_data.save()
                    messages.success(request,'Updated  Successfully')
                    return redirect('edit_time_table')
            
            


    except Exception as e:
        messages.error(request,e)
        return redirect('edit_time_table')



@login_required(login_url='/')
def Delete_Time_Table_Data(request,id):
    time=Time_Table.objects.get(id=id)
    time.delete()
    messages.success(request,'Time Table Deleted Successfully')
    return redirect('edit_time_table')




def Set_Fee(request):

    session_year=Session_year.objects.all()
    Class=S_Clas.objects.all()
    context={
        'session':session_year,
        'class':Class,
    }
    return render(request,'HOD/FEE/set_fee.html',context)


def Add_Fee(request):
    try:

        if request.method=='POST':
            session=request.POST.get('Session_id')
            Class=request.POST.get('S_class_id')
            monthly_fee=request.POST.get('monthly_fee')
            Exam_fee=request.POST.get('exam_fee')
            print(Exam_fee)
            Other_fee=request.POST.get('other_fee')

            session_id=Session_year.objects.get(id=session)
            Class_id=S_Clas.objects.get(id=Class)
            if Exam_fee == 0 :
                set_fee=SetFee(
                    session=session_id,
                    student_class=Class_id,
                    other_fee=Other_fee,

                )
                set_fee.save()
                messages.success(request,'Fee Added Successfully')
                return redirect('set_fee')
            if Other_fee == 0 :
                set_fee=SetFee(
                    session=session_id,
                    student_class=Class_id,
                    exam_fee=Exam_fee,

                )
                set_fee.save()
                messages.success(request,'Fee Added Successfully')
                return redirect('set_fee')
            else:

                set_fee=SetFee(
                    session=session_id,
                    student_class=Class_id,
                    monthly_fee=monthly_fee,
                    exam_fee=Exam_fee,
                    other_fee=Other_fee,

                )
                set_fee.save()
                messages.success(request,'Fee Added Successfully')
                return redirect('set_fee')

        
    except IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e.args):
        # Handle the UNIQUE constraint error
        # For example, you can return a custom error message to the user
         messages.error(request,'Fee For The Class of this session Already added')
         return redirect('set_fee')
        else:
            messages.error(request,e)
            return redirect('set_fee')


def View_Fee(request):

    Class=S_Clas.objects.all()
    Session=Session_year.objects.all()
    context={
        'class':Class,
        'session':Session,
    }


    return render(request,'HOD/FEE/view_fee.html',context) 

def Show_Fee(request):
    try:
        if request.method=='POST':
            Class=request.POST.get('S_class_id')
            Session=request.POST.get('Session_id')
            Class_id=S_Clas.objects.get(id=Class)
            Session_id=Session_year.objects.get(id=Session)
            objget=SetFee.objects.filter(session=Session_id,student_class=Class_id)
           

            
            context={
                'fee_data':objget,
            }
            return render(request,'HOD/FEE/show_fee.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('view_fee')
    
def Edit_Fee(request,id):
    try:

     feeid=SetFee.objects.get(id=id)
    
     context={
     'feeid':feeid,
        
        }
     return render(request,'HOD/FEE/edit_fee.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('view_fee')
def Update_Fee(request,id):
    try:
        now = datetime.now(tz)
        formatted_date = now.strftime("%Y-%m-%d")
        if request.method=='POST':
            monthlyfee=request.POST.get('monthly_fee')
            examfee=request.POST.get('exam_fee')
            otherfee=request.POST.get('other_fee')
            feeset=SetFee.objects.get(id=id)
            feeset.monthly_fee=monthlyfee
            feeset.exam_fee=examfee
            feeset.other_fee=otherfee
            feeset.updated_at=formatted_date
            feeset.save()
            messages.success(request,'Fee Updated Successfully')
        return redirect('view_fee')
    except Exception as e:
        messages.error(request,f'{e}')
        return redirect('view_fee')

def Delete_Fee(request,id):
    fee=SetFee.objects.get(id=id)
    fee.delete()
    messages.success(request,'Fee Deleted Successfully')
    return redirect('view_fee')


def Show_Studets_Fee(request):
    session=Session_year.objects.all()
    Class=S_Clas.objects.all()

    context={
        'session':session,
        'class':Class,
    }
    return render(request,'HOD/FEE/view_fee.html',context)



def Get_Fee(request):
    if request.method == 'POST':
        session_id = request.POST.get('Session_id')
        class_id = request.POST.get('S_class_id')
        session = Session_year.objects.get(id=session_id)
        s_class = S_Clas.objects.get(id=class_id)
        
        # Retrieve all SetFee objects that match the selected session and class
        set_fees = SetFee.objects.filter(session=session, student_class=s_class)
        
        # Retrieve all Student objects that belong to the selected class and session
        students = Student.objects.filter(S_Class_id=s_class, Session_year_id=session)
        
        # Store the unpaid months messages in a list
        unpaid_months_messages = []
        
        for set_fee in set_fees:
            # Retrieve all Payment records that match the current SetFee object
            payments = Payment.objects.filter(set_fee=set_fee)
            
            for student in students:
                # Retrieve the Payment record that matches the current student and SetFee
                payment = payments.filter(student=student.admin.id).last()
                
                if payment:
                    # Get the unpaid months message for the Payment record
                    unpaid_months_message = payment.unpaid_months_message()
                    unpaid_months_messages.append(unpaid_months_message)
                    print(unpaid_months_message)
            
            
        

        # for i in students:
        #     st=Student.objects.get(admin=i.id)
        #     pay=Payment.objects.filter(student=st).get()
        #     unp=pay.get_unpaid_months()
        #     print(unp)

        
        return render(request,'HOD/FEE/fee_to_paid.html')



def Take_Attendence(request):



    Class = S_Clas.objects.all()
    Session=Session_year.objects.all()

    action=request.GET.get('action')
    get_class=None
    get_session=None
    students=None
    if action is not None:
        if request.method=='POST':
            Class_id=request.POST.get('class_id')
            Session_id=request.POST.get('session_year_id')
            if Class_id =="Select Class" or Session_id=="Select Session_Year":
                messages.error(request,'Select Class or Session')
                return redirect('take_attendence')
            else:
            

             get_class=S_Clas.objects.get(id=Class_id)
             get_session=Session_year.objects.get(id=Session_id)

             Class_=S_Clas.objects.filter(id=Class_id)
             Sess=Session_year.objects.filter(id=Session_id)

             
             
             for i , j in zip(Class_,Sess):
                 students=Student.objects.filter(S_Class_id=i,Session_year_id=j)
                 print(students)
                 

                 

    context={
        'S_class':Class,
        'Session_year':Session,
        'get_class': get_class,
        'get_session':get_session,
        'students':students,
        'action':action

    }



    return render(request, 'HOD/attendence/take_attendence.html',context)




def Save_Attendence(request):

    if request.method=='POST':
        Class_id=request.POST.get('class_id')
        Session_id=request.POST.get('session_year_id')
        attendence_date=request.POST.get('date')
        student_id=request.POST.getlist('student_id')
        print(student_id)

        get_class=S_Clas.objects.get(id=Class_id)
        get_session=Session_year.objects.get(id=Session_id)
        
        attedence=Attendence(
            S_class=get_class,
            Attendence_date=attendence_date,
            session_year=get_session
        )
        attedence.save()

        for i in student_id:
            stud_id=i
            int_stud=int(stud_id)
            p_student=Student.objects.get(id=int_stud)
            attedence_report= Attendence_Report(
                student_id=p_student,
                Attedence_id=attedence,
            )
            attedence_report.save()

        messages.success(request,"Attendence added Successfully")
    
        return redirect('take_attendence')


def View_Attendence(request):
    return None
