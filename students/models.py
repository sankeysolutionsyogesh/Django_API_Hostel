from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


    
class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    room_number = models.IntegerField(null=True)
    guardian_contact = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(15)])
    fees_paid = models.FloatField(default=0.0)
    is_paid = models.BooleanField()
    roll_no = models.IntegerField()
