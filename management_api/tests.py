from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase

from management_api.models import Employee, Department, Position, Status

TEST_USERNAME = 'tester'
TEST_PASSWORD = 'TestPassword123'
TEST_EMAIL = 'tester@example.com'
EMPLOYEE_URL = reverse('employee-list')

class ModelTests(TestCase):
    """
    ทดสอบความถูกต้องของโมเดลและการสร้างข้อมูลพื้นฐาน
    (Unit Test)
    """

    def test_department_creation(self):
        """Department ควรถูกสร้างและ __str__ ควรคืนค่าชื่อ"""
        dept = Department.objects.create(name='IT')
        self.assertEqual(str(dept), 'IT')

    def test_position_creation(self):
        """Position ควรถูกสร้างและ __str__ ควรคืนค่าชื่อ"""
        pos = Position.objects.create(name='Developer', salary=60000.00)
        self.assertEqual(str(pos), 'Developer')

    def test_status_creation(self):
        """Status ควรถูกสร้างและ __str__ ควรคืนค่าชื่อ"""
        stat = Status.objects.create(name='Active')
        self.assertEqual(str(stat), 'Active')

    def test_employee_creation(self):
        """Employee ควรถูกสร้างและมีค่าที่ถูกต้อง"""
        dept = Department.objects.create(name='HR')
        pos = Position.objects.create(name='Manager', salary=75000.00)
        stat = Status.objects.create(name='On Leave')
        
        employee = Employee.objects.create(
            name='Alice',
            address='BKK',
            is_manager=True,
            position=pos,
            department=dept,
            status=stat,
        )
        self.assertEqual(employee.name, 'Alice')
        self.assertEqual(str(employee), 'Alice') 

class BaseAPITestSetup(APITestCase):
    """
    Class ฐานสำหรับตั้งค่า User, Token, และข้อมูล Foreign Key สำหรับ API Tests
    """
    
    def setUp(self):
        self.user, created = User.objects.get_or_create(
            username=TEST_USERNAME,
            defaults={
                'password': TEST_PASSWORD,
                'email': TEST_EMAIL,
                'is_staff': True, # ให้สิทธิ์ Staff เหมือนใน Migration
                'is_superuser': False,
            }
        )

        if not created:
             self.user.set_password(TEST_PASSWORD)
             self.user.save()

        Token.objects.filter(user=self.user).delete()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.dept1, _ = Department.objects.get_or_create(name='IT')
        self.dept2, _ = Department.objects.get_or_create(name='HR')
        
        self.pos1, _ = Position.objects.get_or_create(
            name='CEO', 
            defaults={'salary': 150000.00} 
        ) 
        self.pos2, _ = Position.objects.get_or_create(
            name='Developer', 
            defaults={'salary': 60000.00}
        )
        
        self.stat1, _ = Status.objects.get_or_create(name='Active')
        self.stat2, _ = Status.objects.get_or_create(name='Inactive')

        self.employee1 = Employee.objects.create(
            name='Charlie Brown',
            address='Bangkok',
            is_manager=False,
            position=self.pos2,
            department=self.dept2,
            status=self.stat2
        )
        self.employee1_detail_url = reverse('employee-detail', args=[self.employee1.id])
        
        self.new_employee_data = {
            'name': 'Bob Smith',
            'address': 'Chiang Mai',
            'is_manager': True,
            'position': self.pos1.id,
            'department': self.dept1.id,
            'status': self.stat1.id,
        }

class TestEmployeeCRUDAndFiltering(BaseAPITestSetup):
    """ทดสอบ CRUD และ Filtering ของ Employee API (Integration Test)"""

    def test_auth_required_for_access(self):
        """Unauthenticated Request ควรถูกปฏิเสธ (401)"""
        self.client.credentials()
        response = self.client.get(EMPLOYEE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_employee_success(self):
        """สามารถสร้าง Employee ใหม่ได้สำเร็จ (POST)"""
        initial_count = Employee.objects.count()
        response = self.client.post(EMPLOYEE_URL, self.new_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), initial_count + 1) 

    def test_filter_by_position_id(self):
        """สามารถกรอง Employee ด้วย Position ID ได้"""
        response = self.client.get(f'{EMPLOYEE_URL}?position={self.pos2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_filter_by_position_name(self):
        """สามารถกรอง Employee ด้วย Position Name ได้"""
        response = self.client.get(f'{EMPLOYEE_URL}?position_name=Developer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_search_by_employee_name(self):
        """สามารถค้นหา Employee ด้วยชื่อบางส่วน (search_name) ได้"""
        response = self.client.get(f'{EMPLOYEE_URL}?search_name=charlie')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Charlie Brown')

    def test_partial_update_employee(self):
        """สามารถแก้ไข Employee บางส่วน (PATCH) ได้สำเร็จ"""
        patch_data = {'is_manager': True}
        response = self.client.patch(self.employee1_detail_url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data['is_manager'])
        updated_employee = Employee.objects.get(pk=self.employee1.pk)
        self.assertTrue(updated_employee.is_manager)
        
    def test_delete_employee(self):
        """สามารถลบ Employee ได้สำเร็จ (DELETE)"""
        initial_count = Employee.objects.count()
        response = self.client.delete(self.employee1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), initial_count - 1)

class TestDepartmentCRUD(BaseAPITestSetup):
    """ทดสอบ CRUD ของ Department API (Integration Test)"""
    
    def setUp(self):
        super().setUp()
        self.dept_url = reverse('department-list')
        self.detail_url = reverse('department-detail', args=[self.dept1.id])
        self.new_dept_data = {'name': 'Accounting'}
        
    def test_list_departments(self):
        """ดึงรายการ Department ได้"""
        initial_count = Department.objects.count()
        response = self.client.get(self.dept_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), initial_count)
        
    def test_create_department(self):
        """สร้าง Department ใหม่ได้"""
        initial_count = Department.objects.count()
        response = self.client.post(self.dept_url, self.new_dept_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), initial_count + 1)
        
    def test_update_department(self):
        """แก้ไข Department ได้ (PUT)"""
        update_data = {'name': 'Finance & Accounting'}
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dept1.refresh_from_db()
        self.assertEqual(self.dept1.name, 'Finance & Accounting')
        
    def test_delete_department(self):
        """ลบ Department ได้"""
        initial_count = Department.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), initial_count - 1)