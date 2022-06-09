from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(alarm)
admin.site.register(toggle)
admin.site.register(intruder)
admin.site.register(intruder_stat)
admin.site.register(owner)