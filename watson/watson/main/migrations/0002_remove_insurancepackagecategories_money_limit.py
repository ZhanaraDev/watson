# Generated by Django 2.2.4 on 2019-08-24 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancepackagecategories',
            name='money_limit',
        ),
    ]