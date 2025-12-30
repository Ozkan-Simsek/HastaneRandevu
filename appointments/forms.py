from django import forms
from .models import Appointment
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["description", "doctor", "date", "document"] 
        
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Şikayetinizi detaylı yazın..."}),
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "document": forms.FileInput(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].required = False
        self.fields['date'].required = True 
        self.fields['date'].label = "Randevu Tarihi"
        self.fields['document'].label = "Dosya Yükle"
        
        self.fields['date'].initial = datetime.now().date()