# Generated by Django 4.2.4 on 2023-08-04 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_remove_room_id_remove_student_room_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='room_number',
            field=models.IntegerField(null=True),
        ),
    ]