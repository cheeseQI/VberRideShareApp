# login/admin.py

from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Ride)
admin.site.register(models.Vehicle)
# Register your models here.
