from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.students.models import Student


@admin.register(Student)
class CustomAdminClass(ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number']
