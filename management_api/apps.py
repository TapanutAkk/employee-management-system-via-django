from django.apps import AppConfig


class ManagementApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management_api'
    
    def ready(self):
        import management_api.signals
