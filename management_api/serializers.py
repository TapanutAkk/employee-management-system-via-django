from rest_framework import serializers
from .models import Employee, Position, Department, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.ReadOnlyField(source='manager.name', allow_null=True)
    class Meta:
        model = Department
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source='status.name')
    position_name = serializers.ReadOnlyField(source='position.name')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = [
            'id', 
            'name', 
            'address', 
            'is_manager',
            'position_name',
            'department_name',
            'status_name',
        ]
        read_only_fields = ('position_name', 'department_name', 'status_name')