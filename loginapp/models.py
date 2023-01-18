from django.db import models 

# Create your models here.
class UserAccounts(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=500)


class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=500)
    DateOfJoining = models.DateField()
    Department = models.CharField(max_length=500)