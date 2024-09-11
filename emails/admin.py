from django.contrib import admin

from .models import Email, EmailTracking, List, Sent, Subscriber

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(EmailTracking)
admin.site.register(Sent)
