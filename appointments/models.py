from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Status(models.Model):
    name=models.CharField(max_length=10)
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=50)
    speciality=models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(verbose_name="Başlık",max_length=100)
    description=models.TextField(verbose_name="Açıklama")
    date=models.DateTimeField(verbose_name="Randevu Tarihi")
    status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,verbose_name="Durum")
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Doktor")
    document = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name="Rapor/Dosya")
    def __str__(self):
        return f"{self.title} - {self.date}"
    


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    diagnosis = models.CharField(max_length=200, verbose_name="Teşhis")
    medicines = models.TextField(verbose_name="İlaçlar ve Tedavi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.user.username} - Reçete"


