from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PositionViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = router.urls