from django.db import migrations

def create_normal_user(apps, schema_editor):
    """
    สร้างบัญชี Normal User ชื่อ 'tester' พร้อมกำหนด Staff Status และ Permissions
    """
    User = apps.get_model('auth', 'User')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    NORMAL_USER_USERNAME = 'tester'
    NORMAL_USER_PASSWORD = 'TestPassword123'
    NORMAL_USER_EMAIL = 'tester@example.com'
    
    if not User.objects.filter(username=NORMAL_USER_USERNAME).exists():
        user = User.objects.create_user(
            username=NORMAL_USER_USERNAME,
            email=NORMAL_USER_EMAIL,
            password=NORMAL_USER_PASSWORD,
            is_staff=True,
            is_superuser=False
        )
        print(f"\nCreated Normal User: {NORMAL_USER_USERNAME} (Staff Status: True)")

        content_types = ContentType.objects.filter(app_label='management_api')
        
        required_permissions = Permission.objects.filter(
            content_type__in=content_types
        ).filter(
            codename__in=[
                'add_employee', 'change_employee', 'delete_employee', 'view_employee',
                'add_position', 'change_position', 'delete_position', 'view_position',
                'add_department', 'change_department', 'delete_department', 'view_department',
                'add_status', 'change_status', 'delete_status', 'view_status',
            ]
        )
        
        user.user_permissions.set(required_permissions)
        user.save()
        print(f"Assigned {required_permissions.count()} CRUD permissions to {NORMAL_USER_USERNAME}.")

def reverse_create_normal_user(apps, schema_editor):
    """ฟังก์ชันสำหรับลบ User หากมีการย้อน Migration"""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='tester').delete()
    print("\nDeleted Normal User: tester")


class Migration(migrations.Migration):

    dependencies = [
        ('management_api', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_normal_user, reverse_create_normal_user),
    ]