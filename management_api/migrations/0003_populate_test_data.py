from django.db import migrations
from django.utils import timezone

def create_test_data(apps, schema_editor):
    """สร้างข้อมูลทดสอบสำหรับ Status, Position, Employee, และ Department"""
    
    Status = apps.get_model('management_api', 'Status')
    Position = apps.get_model('management_api', 'Position')
    Employee = apps.get_model('management_api', 'Employee')
    Department = apps.get_model('management_api', 'Department')
    
    statuses = [
        Status(name='Resigned'),
        Status(name='Normal'),
        Status(name='In Probation Period'),
        Status(name='Waiting For Onboarding'),
        Status(name='In Recruitment Process'),
    ]
    
    status_normal = Status.objects.create(name='Normal')
    status_probation = Status.objects.create(name='In Probation Period')
    Status.objects.create(name='Resigned')
    Status.objects.create(name='Waiting For Onboarding')
    Status.objects.create(name='In Recruitment Process')
    
    print("\n[Data] Created 3 Statuses.")
    
    Position.objects.create(name='CEO', salary=150000)
    Position.objects.create(name='Senior Developer', salary=80000)
    Position.objects.create(name='Junior Developer', salary=45000)
    Position.objects.create(name='HR Manager', salary=70000)
    
    pos_ceo = Position.objects.get(name='CEO')
    pos_senior = Position.objects.get(name='Senior Developer')
    pos_hr_manager = Position.objects.get(name='HR Manager')
    
    print("[Data] Created 4 Positions.")

    Department.objects.create(
        name='Executive'
    )
    Department.objects.create(
        name='Human Resources'
    )

    dept_executive = Department.objects.get(name='Executive')
    dept_hr = Department.objects.get(name='Human Resources')
    
    print("[Data] Created 2 Departments.")

    manager_employee = Employee.objects.create(
        name='CEO Admin', 
        address='Head Office, Bangkok', 
        is_manager=True,
        status=status_normal,
        position=pos_ceo,
        department=dept_executive
    )
    
    hr_manager_employee = Employee.objects.create(
        name='HR Manager Tapanut', 
        address='HR Dept, Floor 5', 
        is_manager=True,
        status=status_normal,
        position=pos_hr_manager,
        department=dept_hr
    )
    
    Employee.objects.create(
        name='Developer Jack', 
        address='Remote Office', 
        is_manager=False,
        status=status_probation,
        position=pos_senior,
        department=dept_executive
    )

    print("[Data] Created 3 Employees (2 managers, 1 staff).")

def reverse_create_test_data(apps, schema_editor):
    """ลบข้อมูลทั้งหมดที่สร้างโดย Migration นี้"""
    Status = apps.get_model('management_api', 'Status')
    Position = apps.get_model('management_api', 'Position')
    Employee = apps.get_model('management_api', 'Employee')
    Department = apps.get_model('management_api', 'Department')
    
    Status.objects.all().delete()
    Position.objects.all().delete()
    Department.objects.all().delete()
    Employee.objects.filter(name__in=['CEO Admin', 'HR Manager Tapanut', 'Developer Jack']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('management_api', '0002_create_normal_user'), 
    ]

    operations = [
        migrations.RunPython(create_test_data, reverse_create_test_data),
    ]