from django.db import migrations

def create_normal_user(apps, schema_editor):
    """
    สร้างบัญชี Normal User ชื่อ 'tester' พร้อมกำหนด Staff Status และ Permissions
    """
    User = apps.get_model('auth', 'User')

    ADMIN_USER_USERNAME = 'admin'
    ADMIN_USER_PASSWORD = 'AdminPassword123'
    ADMIN_USER_EMAIL = 'admin@example.com'

    try:
        user = User.objects.get(username=ADMIN_USER_USERNAME)
        print(f"\nUser '{ADMIN_USER_USERNAME}' already exists.")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=ADMIN_USER_USERNAME,
            email=ADMIN_USER_EMAIL,
            password=ADMIN_USER_PASSWORD,
            is_staff=True,
            is_superuser=True
        )
        print(f"\nCreated Super User: {ADMIN_USER_EMAIL} (Staff Status: True)") 
    
    NORMAL_USER_USERNAME = 'tester'
    NORMAL_USER_PASSWORD = 'TestPassword123'
    NORMAL_USER_EMAIL = 'tester@example.com'

    try:
        user = User.objects.get(username=NORMAL_USER_USERNAME)
        print(f"\nUser '{NORMAL_USER_USERNAME}' already exists.")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=NORMAL_USER_USERNAME,
            email=NORMAL_USER_EMAIL,
            password=NORMAL_USER_PASSWORD,
            is_staff=True,
            is_superuser=False
        )
        print(f"\nCreated Normal User: {NORMAL_USER_USERNAME} (Staff Status: True)") 

def reverse_create_normal_user(apps, schema_editor):
    """ฟังก์ชันสำหรับลบ User หากมีการย้อน Migration"""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()
    print("\nDeleted Super User: tester")
    User.objects.filter(username='tester').delete()
    print("\nDeleted Normal User: tester")


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('management_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_normal_user, reverse_create_normal_user),
    ]