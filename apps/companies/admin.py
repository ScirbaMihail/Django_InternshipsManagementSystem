from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.companies.models import Company


@admin.register(Company)
class CustomAdminClass(ModelAdmin):
    list_display = ["name", "web_url", "email"]
