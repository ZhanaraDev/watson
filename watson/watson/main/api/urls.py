from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InsurancePackageViewset, CategoryViewset, ProfileViewset, ServiceProviderViewset, AppointmentViewSet

router = DefaultRouter()
router.register(r'insurance_package', InsurancePackageViewset)
router.register(r'category', CategoryViewset)
router.register(r'profile', ProfileViewset)
router.register(r'service_provider', ServiceProviderViewset)
router.register(r'appointment', AppointmentViewSet)

urlpatterns = router.urls
