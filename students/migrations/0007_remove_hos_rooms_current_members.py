# Generated by Django 4.2.4 on 2023-08-04 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_hos_rooms_alter_student_room_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hos_rooms',
            name='current_members',
        ),
    ]