from django.contrib import admin

from .models import Customer, Employee, Student

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Student)
# Register your models here.
