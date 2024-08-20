from django.contrib import admin

# Register your models here.
from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ["id", "model_name", "created_at"]
    ordering = ["-id"]
