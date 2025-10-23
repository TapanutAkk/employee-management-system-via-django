from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver

@receiver(post_migrate, sender=apps.get_app_config('management_api'))
def assign_staff_permissions(sender, **kwargs):
    """กำหนดสิทธิ์ให้กับ Normal User (tester) หลัง migrate เสร็จแล้ว"""
    User = apps.get_model('auth', 'User')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    NORMAL_USER_USERNAME = 'tester'

    try:
        user = User.objects.get(username=NORMAL_USER_USERNAME)
    except User.DoesNotExist:
        return

    if user.is_staff:
        model_names = ['employee', 'position', 'department', 'status']
        required_permissions = []

        for model_name in model_names:
            try:
                content_type = ContentType.objects.get(
                    app_label='management_api', 
                    model=model_name
                )

                for action in ['add', 'change', 'delete', 'view']:
                    codename = f'{action}_{model_name}'
                    perm = Permission.objects.get(
                        codename=codename, 
                        content_type=content_type
                    )
                    required_permissions.append(perm)

            except Exception as e:
                print(f"Error finding permissions for {model_name}: {e}")
                continue

        user.user_permissions.set(required_permissions)
        user.save()
        print(f"Signal: Assigned {len(required_permissions)} CRUD permissions to {NORMAL_USER_USERNAME} via post_migrate.")