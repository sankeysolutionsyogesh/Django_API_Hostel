# Generated by Django 4.2.4 on 2023-08-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20230803_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='guardian_contact',
            field=models.IntegerField(max_length=15),
        ),
    ]
