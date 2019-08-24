from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InsurancePackageViewset


router = DefaultRouter()
router.register(r'insurance_package', InsurancePackageViewset)

urlpatterns = router.urls