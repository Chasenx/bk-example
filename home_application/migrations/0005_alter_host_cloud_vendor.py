# Generated by Django 3.2.4 on 2024-03-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_alter_host_bak_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='cloud_vendor',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
