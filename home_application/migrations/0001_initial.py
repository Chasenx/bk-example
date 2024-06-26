# Generated by Django 3.2.4 on 2024-03-04 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TestModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.CharField(max_length=200)),
                ("count", models.IntegerField()),
                ("pub_date", models.DateTimeField(verbose_name="date published")),
            ],
        ),
    ]
