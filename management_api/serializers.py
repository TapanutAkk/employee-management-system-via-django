from rest_framework import serializers
from .models import Employee, Position, Department, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.ReadOnlyField(source='manager.name', allow_null=True)
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source='status.name')
    position_name = serializers.ReadOnlyField(source='position.name')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = '__all__'