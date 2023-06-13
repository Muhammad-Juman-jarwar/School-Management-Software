from datetime import datetime
import pytz
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from School_sys.models import Teachers,Teachers_Notification,Teachers_Leave,Time_Table,S_Clas,Session_year,Subject
from django.contrib import messages


from .tables import ForTeacherTimeTableTable




@login_required(login_url='/')
def Home(request):
    return render(request,'TEACHERS/Home.html')
@login_required(login_url='/')
def Notifications(request):
    teacher= Teachers.objects.filter(admin = request.user.id)
    
    for i in teacher:
        teacher_id=i.id
      

        teacher_notification=Teachers_Notification.objects.filter(teacher_id = teacher_id)
        context={
            'notification':teacher_notification,
        }
        return render(request,'TEACHERS/Notifications.html',context)

@login_required(login_url='/')
def Mark_As_Done(request,status):
    
    try:
        status=Teachers_Notification.objects.get(id=status)

        status.status= 1
        status.save()

        return redirect('notifications')
    except Exception as e:

        messages.error(request,e)
        return redirect('notifications')




@login_required(login_url='/')
def Tecaher_Apply_Leave(request):

    

    teacher_leave=Teachers.objects.get(admin=request.user.id)
    teacher_got=Teachers_Leave.objects.filter(Teacher_id=teacher_leave)
    context={
        'leave_date':teacher_got,
    }



    return render(request,'TEACHERS/Teacher_Leave.html',context)

@login_required(login_url='/')
def Teacher_Apply_Leave_Save(request):
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
                return redirect('teacher_apply_leave')
            else:
                Teacher= Teachers.objects.get(admin=request.user.id)
                leave=Teachers_Leave(
                    Teacher_id=Teacher,
                    date_from=leave_from,
                    date_to=leave_to,
                    message=leave_message
                )
                leave.save()
                messages.success(request,"Application Applied for leave Successfully")
                return redirect('teacher_apply_leave')





    except Exception as e:
        messages.error(request,e)
        return redirect('teacher_apply_leave')



def Show_Teacher_Time_Table(request):
    id=request.user.id

    teacher=Teachers.objects.get(admin=id)
    time_table_data =Time_Table.objects.filter(Teacher_id=teacher)
    table= ForTeacherTimeTableTable(time_table_data)
    return render(request, 'TEACHERS/generated_time_table.html',{'table':table})
