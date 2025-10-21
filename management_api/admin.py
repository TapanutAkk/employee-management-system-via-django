from django.contrib import admin
from .models import Employee, Position, Department, Status

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Status)