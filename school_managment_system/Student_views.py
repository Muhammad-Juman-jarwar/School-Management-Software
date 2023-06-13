from datetime import datetime
import pytz
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from School_sys.models import S_Clas, Session_year, CustomUser ,Student,Student_Notification,Students_Leave,Time_Table,Teachers
from django.contrib import messages
from .tables import StudentTimeTableTable

@login_required(login_url='/')
def Home(request):
    return render(request,'Student/home.html')


@login_required(login_url='/')
def View_Notification(request):
    try:

        Stud_class=Student.objects.get(admin=request.user.id)
        cl=Stud_class.S_Class_id
        ses=Stud_class.Session_year_id
        notification=Student_Notification.objects.filter(Class=cl,session=ses).values('id','message','status','created_at')
        context={
        'Class':cl,
        'session':ses,
        'messag':notification,

        }


        return render(request,'Student/View_notification.html',context)
    except Exception as e:
        messages.error(request,e)
        return redirect('student_home')
    
def Mark_As_Read(request,status):
    try:
        status=Student_Notification.objects.get(id=status)
        status.status=1
        status.save()
        return redirect('view_notifications')
    except Exception as e:
        messages.error(request,e)
        return redirect('view_notifications')
    
def Student_Apply_Leave(request):
    user_id=request.user.id
    
    student=Student.objects.get(admin=user_id)

    student_got=Students_Leave.objects.filter(Student_id=student)
    Class=student.S_Class_id
    ses_id=student.Session_year_id.id
    session=Session_year.objects.get(id=ses_id)
    

   
    

    context={
        'Class':Class,
        'session':session,
        'leave_date':student_got,
       

    }

    return render(request,'Student/student_leave.html',context)




def Student_Save_Leave(request):
    try:
        if request.method == "POST":
            tz = pytz.timezone('Asia/Karachi')
            now = datetime.now(tz)
            formatted_date = now.strftime("%Y-%m-%d")
            leave_from= request.POST.get('leave_from')
            leave_to= request.POST.get('leave_to')
            leave_message= request.POST.get('leave_message')
            if leave_from<formatted_date or leave_to<leave_from:
                messages.warning(request,"Invalid Date Selection")
                return redirect('student_apply_leave')
            else:
                student= Student.objects.get(admin=request.user.id)
                leave=Students_Leave(
                    Student_id=student,
                    date_from=leave_from,
                    date_to=leave_to,
                    message=leave_message
                )
                leave.save()
                messages.success(request,"Application Applied for leave Successfully")
                return redirect('student_apply_leave')
            
    except Exception as e:
           messages.error(request,e)
           return redirect('student_apply_leave')


def Show_Student_Time_Table(request):
    stid=Student.objects.get(admin=request.user.id)
    teacher=Teachers.objects.all()
    Class=S_Clas.objects.all()
    Session=Session_year.objects.all()
    # for h in teacher:
    #     print(h)
    for i , j,k in zip(Class,Session,teacher):
        Class_id=S_Clas.objects.get(id=i.id)
        Session_id=Session_year.objects.get(id=j.id)
        time_table_data =Time_Table.objects.filter(CLass=stid.S_Class_id,Session_year_id=stid.Session_year_id)

        table= StudentTimeTableTable(time_table_data)
        return render(request, 'Student/Show_Time_Table.html',{'table':table})


