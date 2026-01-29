from django.contrib import admin
from .models import Appointment, Status, Doctor

admin.site.register(Status)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality')
    search_fields = ('name', 'speciality')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'status')
    list_filter = ('status', 'doctor', 'date')
    search_fields = ('user__username', 'doctor__name')
