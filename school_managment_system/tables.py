from django_tables2 import tables
from School_sys.models import Time_Table

from django_tables2.export.views import ExportMixin

class TimeTableTable(tables.Table):
    subject = tables.columns.Column()
    teacher = tables.columns.Column(accessor='Teacher_id')  # use the Teacher_id field instead of Teacher
    session = tables.columns.Column(accessor='Session_year_id')  
    class_name = tables.columns.Column(accessor='CLass')  # use the CLass field instead of Class
    day = tables.columns.Column()
    start_time = tables.columns.Column()
    end_time = tables.columns.Column()

    class Meta:
        model = Time_Table
        fields = ('subject', 'teacher', 'class_name', 'day', 'start_time', 'end_time')
        template_name = 'django_tables2/bootstrap4.html'  # use the bootstrap4 template

   


class ForTeacherTimeTableTable(tables.Table):
    subject = tables.columns.Column()
    teacher = tables.columns.Column(accessor='Teacher_id')  # use the Teacher_id field instead of Teacher
    session = tables.columns.Column(accessor='Session_year_id')
    class_name = tables.columns.Column(accessor='CLass')  # use the CLass field instead of Class
    day = tables.columns.Column()
    start_time = tables.columns.Column()
    end_time = tables.columns.Column()

    class Meta:
        model = Time_Table
        fields = ('subject', 'teacher', 'class_name', 'day', 'start_time', 'end_time')
        template_name = 'django_tables2/bootstrap4.html'  # use the bootstrap4 template


class StudentTimeTableTable(tables.Table):
    subject = tables.columns.Column()
    teacher = tables.columns.Column(accessor='Teacher_id')  # use the Teacher_id field instead of Teacher
    session = tables.columns.Column(accessor='Session_year_id')  
    class_name = tables.columns.Column(accessor='CLass')  # use the CLass field instead of Class
    day = tables.columns.Column()
    start_time = tables.columns.Column()
    end_time = tables.columns.Column()

    class Meta:
        model = Time_Table
        fields = ('subject', 'teacher', 'class_name', 'day', 'start_time', 'end_time')
        template_name = 'django_tables2/bootstrap4.html'  # use the bootstrap4 templat