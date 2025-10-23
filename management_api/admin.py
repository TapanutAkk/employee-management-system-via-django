from django.contrib import admin
from .models import Employee, Position, Department, Status

from django import forms

class DepartmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = Employee.objects.filter(is_manager=True)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Department, DepartmentAdmin)

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Status)