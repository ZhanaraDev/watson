# Generated by Django 2.2.4 on 2019-08-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_clientcompanyemployees_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='avatar',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='categories',
            field=models.ManyToManyField(to='main.Category'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='position',
            field=models.CharField(default='therapist', max_length=250),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='surname',
            field=models.CharField(default='', max_length=250),
        ),
    ]
