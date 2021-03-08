from django.db import models

# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile=models.CharField(max_length=10)
    auth_token=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    employee_id=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=20)


    def __str__(self):
        return self.user_name



class Customer_department(models.Model):
    dept_name = models.CharField(max_length=100)


    def __str__(self):
        return self.dept_name

