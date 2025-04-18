from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.applications.models import Application


@admin.register(Application)
class CustomAdminClass(ModelAdmin):
    list_display = ['student__first_name', 'student__last_name', 'internship__name', 'status']
