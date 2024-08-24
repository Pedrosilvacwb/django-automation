from django.contrib import admin

from .models import Email, List, Subscriber

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
