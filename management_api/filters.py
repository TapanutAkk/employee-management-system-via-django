import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    """
    Filter Class สำหรับโมเดล Employee
    รองรับการกรองตาม FK (Position, Department, Status) และการค้นหาชื่อ (Name)
    """
    
    search_name = django_filters.CharFilter(
        field_name='name', 
        lookup_expr='icontains',
        label='Search by Employee Name'
    )

    position_name = django_filters.CharFilter(
        field_name='position__name',
        lookup_expr='exact',
        label='Filter by Position Name'
    )
    
    # ⬅️ 2. เพิ่ม filter สำหรับ Department Name
    department_name = django_filters.CharFilter(
        field_name='department__name',
        lookup_expr='exact',
        label='Filter by Department Name'
    )

    status_name = django_filters.CharFilter(
        field_name='status__name',
        lookup_expr='exact',
        label='Filter by Status Name'
    )

    class Meta:
        model = Employee
        fields = {
            'position': ['exact'], 
            'department': ['exact'],
            'status': ['exact'], 
        }