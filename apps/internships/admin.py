from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.internships.models import Internship


@admin.register(Internship)
class CustomAdminClass(ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
