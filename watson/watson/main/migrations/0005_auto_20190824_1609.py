# Generated by Django 2.2.4 on 2019-08-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190824_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='categories',
            field=models.ManyToManyField(null=True, to='main.Category'),
        ),
    ]
