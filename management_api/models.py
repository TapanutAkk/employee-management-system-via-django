from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(
        'Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_departments'
    )

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    is_manager = models.BooleanField(default=False) # manager (Y/N)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    def __str__(self):
        return self.name