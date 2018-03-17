from django.contrib import admin

# Register your models here.
from .models import Pool, Response, Notification

admin.site.register(Pool)
admin.site.register(Response)
admin.site.register(Notification)
