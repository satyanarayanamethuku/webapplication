from django.contrib import admin
from .models import Employee,Customer_department
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name','user_name', 'email','mobile','auth_token','created_at','is_verified','employee_id','password']

admin.site.register(Employee,EmployeeAdmin)

admin.site.register(Customer_department)