from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Position, Department
from .serializers import EmployeeSerializer, PositionSerializer, DepartmentSerializer
from .filters import EmployeeFilter

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated] 

    filterset_class = EmployeeFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['position', 'department', 'status']
    search_fields = ['name', 'address'] 

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]