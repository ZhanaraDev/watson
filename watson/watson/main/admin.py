from django.contrib import admin

# Register your models here.
from main.models import Category, InsurancePackage, InsurancePackageCategories

admin.site.register(Category)
admin.site.register(InsurancePackage)
admin.site.register(InsurancePackageCategories)