# Generated by Django 2.2.4 on 2019-08-24 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_insurancepackagecategories_money_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcompanyemployees',
            name='avatar',
            field=models.CharField(default='', max_length=500),
        ),
    ]
