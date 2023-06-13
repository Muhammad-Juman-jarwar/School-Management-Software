from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from datetime import date,datetime,timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import calendar
from apscheduler.schedulers.background import BackgroundScheduler
import datetime



# Create your models here.

class CustomUser(AbstractUser):
    USERS =(
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT'),

    )

    
    user_type=models.CharField(choices=USERS,max_length=50, default=1)
    profile_pic= models.ImageField(upload_to='media/profile_pic')
 

class S_Clas(models.Model):
    name =  models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Session_year(models.Model):
    Session_start=models.CharField(max_length=100,null=True)
    Session_end=models.CharField(max_length=100,null=True)

    def formatted_date(self):
        return datetime.strptime(self.Session_start, '%m/%d/%Y').date() and datetime.strptime(self.Session_end, '%m/%d/%Y').date()
    
    def __str__(self) :
            return self.Session_start+ "TO" +self.Session_end


class Student(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address= models.TextField()
    Gender = models.CharField(max_length=100)
    Father_Name=models.CharField(max_length=100)
    DOB= models.DateField(max_length=10)
    S_Class_id = models.ForeignKey(S_Clas,on_delete=models.SET_NULL, null=True, blank=True)
    Session_year_id = models.ForeignKey(Session_year,on_delete=models.SET_NULL, null=True, blank=True)
    fee_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self) :
        return self.admin.first_name+""+self.admin.last_name
    def save(self, *args, **kwargs):

        if self.S_Class_id and self.Session_year_id:
            set_fees = SetFee.objects.filter(student_class=self.S_Class_id, session=self.Session_year_id).last()
            set_pay = Payment.objects.filter(student__S_Class_id=self.S_Class_id, set_fee__session=self.Session_year_id).last()
            if set_fees:
                self.fee_balance += set_fees.monthly_fee
            if set_pay:
                self.fee_balance -= set_pay.amount
                

        super().save(*args, **kwargs)






class Teachers(models.Model):
     admin= models.OneToOneField(CustomUser,on_delete=models.CASCADE)
     address= models.TextField()
     Father_Name=models.CharField(default=None,max_length=100)
     contact = models.CharField(max_length=100)
     gender=models.CharField(max_length=100)
     created_at=models.DateTimeField(default=timezone.now)
     updated_at=models.DateTimeField(default=timezone.now)

     def __str__(self):
         
         return self.admin.username
     

class Subject(models.Model):
     name = models.CharField( max_length=100)
     created_at=models.DateTimeField(default=timezone.now)
     updated_at=models.DateTimeField(default=timezone.now)

     def __str__(self) :
          return self.name


          
class Teachers_Notification(models.Model):
     teacher_id=models.ForeignKey(Teachers,on_delete=models.CASCADE)
     message=models.TextField()
     created_at=models.DateTimeField(default=timezone.now)
     status=models.IntegerField(null=True,default=0)

     def __str__(self) :
          return self.teacher_id.admin.first_name


class Teachers_Leave(models.Model):
     Teacher_id=models.ForeignKey(Teachers,on_delete=models.CASCADE)
     date_from=models.CharField(max_length=100,null=True)
     date_to=models.CharField(max_length=100,null=True)
     message=models.TextField()
     status=models.IntegerField(default=0)
     created_at=models.DateTimeField(default=timezone.now)
     updated_at=models.DateTimeField(default=timezone.now)

     def __str__(self):
          return self.Teacher_id.admin.first_name + self.Teacher_id.admin.last_name


class Student_Notification(models.Model):
     Class=models.ForeignKey(S_Clas,on_delete=models.CASCADE)
     session=models.ForeignKey(Session_year,on_delete=models.CASCADE)
     message=models.TextField()
     created_at=models.DateTimeField(default=timezone.now)
     status=models.IntegerField(null=True,default=0)

     def __str__(self) :
          return self.Class.name +" "+ self.session.Session_start + self.session.Session_end


class Students_Leave(models.Model):
     Student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
     date_from=models.CharField(max_length=100,null=True)
     date_to=models.CharField(max_length=100,null=True)
     message=models.TextField()
     status=models.IntegerField(default=0)
     created_at=models.DateTimeField(default=timezone.now)
     updated_at=models.DateTimeField(default=timezone.now)

     def __str__(self):
          return self.Student_id.admin.first_name + self.Student_id.admin.last_name


class Time_Table(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    Teacher_id=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    CLass= models.ForeignKey(S_Clas,on_delete=models.CASCADE)
    Session_year_id = models.ForeignKey(Session_year,on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.CLass}) - {self.day} {self.start_time}-{self.end_time}"




class SetFee(models.Model):
    session = models.ForeignKey(Session_year, on_delete=models.CASCADE)
    student_class = models.ForeignKey(S_Clas, on_delete=models.CASCADE)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=False)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=False)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=False)
    start_month = models.CharField(max_length=20,default='N/A')
    end_month = models.CharField(max_length=20,default='N/A')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    class Meta:
        unique_together = ('session', 'student_class')
     
    def __str__(self):

        return f"{self.student_class}- {self.session}-'fees'  "
    

    def clean(self):
        super().clean()
        if not (self.exam_fee or self.monthly_fee or self.other_fee):
            raise ValidationError(_('At least one fee amount must be set.'))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
        # Update fee balance of all students for this set fee
            students = Student.objects.filter(S_Class_id=self.student_class, Session_year_id=self.session).distinct()
            print(f"Updating fee balance for {students.count()} students")
            for student in students:
                student.fee_balance += self.exam_fee + self.monthly_fee + self.other_fee
                student.save()
                print(f"Updated fee balance for student {student.admin.id}: {student.fee_balance}")
    
    def add_monthly_fee(self):
        today = date.today()
        current_month = today.month
        last_month = current_month - 1 if current_month > 1 else 12
        for student in Student.objects.filter(Q(S_Class_id__isnull=False) & Q(Session_year_id__isnull=False)).exclude(payment__set_fee__start_month=current_month).distinct():
            set_fee = SetFee.objects.filter(student_class=student.S_Class_id, session=student.Session_year_id).last()
            # Check if the student has not paid for the last month
            if not set_fee:
                continue
            last_payment = Payment.objects.filter(student=student, Student__S_Class_id=SetFee.student_class, Student__Session_year_id=SetFee.session).last()
            if not last_payment:
                payment = Payment.objects.create(student=student, set_fee=set_fee, amount=set_fee.monthly_fee, description="Monthly fee")
                student.fee_balance += set_fee.monthly_fee
                student.save()
                payment.save()



        


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    set_fee = models.ForeignKey(SetFee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
       
    def __str__(self):
        return f"{self.student.admin.first_name} + paid on {self.month_name()}"
    
    def month_name(self):
        return self.date.strftime("%B")

    def save(self, *args, **kwargs):
        # Update the student's fee balance when a new payment is made
        self.student.fee_balance -= self.amount
        self.student.save()
        super().save(*args, **kwargs)

    def get_unpaid_months(self):
        """
        Returns the number of months for which the student has not paid their fee.
        """
        last_payment = Payment.objects.filter(student=self.student, set_fee=self.set_fee).exclude(pk=self.pk).last()
        if not last_payment:
            return 0
        
        last_month_paid = last_payment.date.month
        current_month = self.date.month
        months_diff = (current_month - last_month_paid) % 12
        if months_diff == 0:
            return 0
        else:
            return months_diff
    
    def unpaid_months_message(self):
        """
        Returns a message indicating the number of months for which the student has not paid their fee.
        """
        months = self.get_unpaid_months()
        if months == 0:
            return ""
        elif months == 1:
            return "Unpaid for 1 month"
        else:
            return f"Unpaid for {months} months"

    class Meta:
        ordering = ['-date']






# now = datetime.datetime.now()
# time_to_set = datetime.time(hour=10, minute=0, second=0)
# now = datetime.datetime.combine(now.date(), time_to_set)
# # last_day_of_month = datetime.date(now.year, now.month, 1) + datetime.timedelta(days=32) - datetime.timedelta(days=1)
# setFee=SetFee()
# if now.time ==now:
#         setFee.add_monthly_fee()
#         # last_day_of_month = datetime.date(now.year, now.month, 1) + datetime.timedelta(days=32) - datetime.timedelta(days=1)



class Attendence(models.Model):
    S_class=models.ForeignKey(S_Clas,on_delete=models.DO_NOTHING)
    Attendence_date=models.DateField()
    session_year=models.ForeignKey(Session_year,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.S_class.name
    

class Attendence_Report(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    Attedence_id=models.ForeignKey(Attendence,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.student_id.admin.first_name
    