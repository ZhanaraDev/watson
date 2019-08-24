from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_legth=250)
    description = models.TextField()


class ClientCompany(models.Model):
    name = models.CharField(max_length=250)
    money_paid = models.DecimalField()


class InsurancePackage(models.Model):
    package_name = models.CharField(max_length=250)


class InsurancePackageCategories(models.Model):
    category = models.ForeignKey(Category)
    package = models.ForeignKey(InsurancePackage)
    money_limit = models.DecimalField()


class ClientCompanyEmployees(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(ClientCompany)
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    iin = models.CharField(max_length=250)
    balance = models.DecimalField()
    insurance_package = models.OneToOneField(InsurancePackage, null=True)


class ServiceProvidingHolding(models.Model):
    name = models.CharField(max_length=250)


class ServiceProvider(models.Model):
    name = models.CharField()
    hospital = models.ForeignKey(ServiceProvidingHolding)
    visit_cost = models.DecimalField()


DAY_CHOICES = (
        ('mon', u'Понедельник'),
        ('tue', u'Вторник'),
        ('wed', u'Среда'),
        ('thu', u'Четверг'),
        ('fri', u'Пятница'),
        ('sat', u'Суббота'),
        ('sun', u'Воскресенье'),
    )


class ServiceProviderSchedule(models.Model):
    service_provider = models.ForeignKey(ServiceProvider)
    day = models.CharField(choices=DAY_CHOICES)
    time_start = models.DateField()
    time_end = models.DateField()


class Appointment(models.Model):
    employee = models.ForeignKey(ClientCompany)
    service_provider = models.ForeignKey(ServiceProvider)
    date = models.DateField()
    time = models.TimeField()
    week_day = models.CharField(choices=DAY_CHOICES)
