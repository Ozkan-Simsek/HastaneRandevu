from django.contrib import admin
from .models import Appointment,Status,Doctor
# Register your models here.

admin.site.register(Status)

class AppointmentAdmin(admin.ModelAdmin):
    list_display=("title","date","user","status","doctor")
    list_filter=("status",)

admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Doctor)

