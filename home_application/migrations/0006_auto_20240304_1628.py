# Generated by Django 3.2.4 on 2024-03-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_alter_host_cloud_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='bak_operator',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='host',
            name='cloud_vendor',
            field=models.CharField(default='', max_length=100),
        ),
    ]