import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()


class ClientCompany(models.Model):
    name = models.CharField(max_length=250)
    money_paid = models.DecimalField(max_digits=8, decimal_places=2)


class InsurancePackage(models.Model):
    package_name = models.CharField(max_length=250)
    is_base = models.BooleanField(default=False)


class InsurancePackageCategories(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    package = models.ForeignKey(InsurancePackage, on_delete=models.CASCADE)


class ClientCompanyEmployees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(ClientCompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    iin = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    insurance_package = models.OneToOneField(InsurancePackage, null=True, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500, default='')


class ServiceProvidingHolding(models.Model):
    name = models.CharField(max_length=250)


class ServiceProvider(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250, default="")
    position = models.CharField(max_length=250, default="therapist")
    service_providing_holding = models.ForeignKey(ServiceProvidingHolding, on_delete=models.CASCADE)
    visit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    avatar = models.CharField(max_length=250, default="")
    categories = models.ManyToManyField(Category, null=True)


DAY_CHOICES = (
        ('mon', u'Понедельник'),
        ('tue', u'Вторник'),
        ('wed', u'Среда'),
        ('thu', u'Четверг'),
        ('fri', u'Пятница'),
        ('sat', u'Суббота'),
        ('sun', u'Воскресенье'),
    )

WEEK_DICT = {
        'mon': 1,
        'tue': 2,
        'wed': 3,
        'thu': 4,
        'fri': 5,
        'sat': 6,
        'sun': 7,
}


class ServiceProviderSchedule(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICES, max_length=50)
    time_start = models.TimeField(default=datetime.time(hour=9))
    time_end = models.TimeField(default=datetime.time(hour=18))


class Appointment(models.Model):
    employee = models.ForeignKey(ClientCompanyEmployees, on_delete=models.CASCADE, null=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    week_day = models.CharField(choices=DAY_CHOICES, max_length=50)
