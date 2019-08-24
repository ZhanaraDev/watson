from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InsurancePackageViewset, CategoryViewset


router = DefaultRouter()
router.register(r'insurance_package', InsurancePackageViewset)
router.register(r'category', CategoryViewset)

urlpatterns = router.urls