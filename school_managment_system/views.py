from django.shortcuts import render,redirect,HttpResponse
from School_sys.EmailBackend import EmailBackend
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from School_sys.models import CustomUser



def BASE(request):
    return render(request,'base.html')
def LOGIN(request):
    return render(request,'login.html')
def doLogin(request):
    if request.method == "POST":
        user = EmailBackend.authenticate(request, 
        username=request.POST.get('email'),
        password=request.POST.get('password'),)

        if user!=None:
            login(request,user)
            user_type= user.user_type
            if user_type =='1':
                return redirect('hod_home')
            elif user_type=='2':
                return redirect('teacher_home')
                
            elif user_type=='3':
                return redirect('student_home')
            else:
                messages.error(request, 'Invalid Email or Password ')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email or Password ')

            return redirect('login')
def doLogout(request):
    logout(request)
    return redirect('login')

def Profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context={
        "user":user,

    }
    return render(request,'profile.html',context)
def Profile_Update(request):
    if request.method=="POST":
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        Username= request.POST.get('user_name')
        Password= request.POST.get('password')
    
        try:
         customUser =CustomUser.objects.get(id=request.user.id)
         customUser.first_name=first_name
         customUser.last_name=last_name
        #  customUser.profile_pic=profile_pic
         if Password!=None and Password != "":
            customUser.set_password(Password)
         if profile_pic!=None and profile_pic!= "":
            customUser.profile_pic=profile_pic
         customUser.save()
         messages.success(request,"Profile Updated Succesfully!!")
         return redirect('profile')
        except:
            messages.error(request,"faied to update")

    return render(request,'profile.html')

