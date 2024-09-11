from django.contrib import admin
from django.utils.html import format_html

from .models import CompressImage


class CompressImageAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(
            f'<img src="{obj.compressed_image.url}" width="40" height="40" />'
        )

    def original_image_size(self, obj):
        return format_html(f"{obj.original_img.size / (1024*1024):.2f} MB")

    def compressed_image_size(self, obj):
        size_in_mb = obj.compressed_image.size / (1024 * 1024)
        if size_in_mb > 1:
            size = size_in_mb
        else:
            size = obj.compressed_image.size / 1024
        return format_html(f"{size:.2f} {'MB' if size_in_mb > 1 else 'KB'}")

    list_display = (
        "user",
        "thumbnail",
        "original_image_size",
        "compressed_image_size",
        "compressed_at",
    )


admin.site.register(CompressImage, CompressImageAdmin)
# Register your models here.
