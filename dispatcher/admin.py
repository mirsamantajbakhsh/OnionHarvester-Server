from django.contrib import admin

# Register your models here.
from .models import Pool, Response

admin.site.register(Pool)
admin.site.register(Response)
