from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('director', 'Director'),
        ('supervisor', 'Supervisor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    matric_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    registration_date = models.DateField(default=date.today)


class PostingPlace(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervised_places', null=True, blank=True)

    def __str__(self):
        return self.name

class StudentApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', null=True)
    posting_place = models.ForeignKey(PostingPlace, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    director_approval = models.BooleanField(default=False)
    work_completed = models.BooleanField(default=False, null=True, blank=True)
    payment_status = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.posting_place.name}"



class WorkStatus(models.Model):
    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='work_statuses', null=True)
    week_number = models.IntegerField()
    student_checked = models.BooleanField(default=False)
    supervisor_checked = models.BooleanField(default=False)
    checked_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Week {self.week_number} - {self.application.student.username} - {self.supervisor_checked}"


class BankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Bank Details for {self.user.username}: {self.bank_name}, \
        {self.account_number}, {self.account_name}"


