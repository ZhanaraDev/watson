from django.contrib import admin

# Register your models here.
from main.models import Category, InsurancePackage, InsurancePackageCategories, ServiceProviderSchedule, Appointment

admin.site.register(Category)
admin.site.register(InsurancePackage)
admin.site.register(InsurancePackageCategories)
admin.site.register(ServiceProviderSchedule)
admin.site.register(Appointment)
