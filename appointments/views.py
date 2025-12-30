from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db.models import Q
from django.core.mail import send_mail
from .forms import AppointmentForm
from .models import Appointment, Doctor, Status
from .utils import get_ai_specialty, check_emergency
from django.db.models import Count


def get_available_slots(doctor, check_date):
    """
    Seçilen doktor ve tarih için 09:00 - 17:00 arası boş slotları üretir.
    """
    slots = []
    start_time = time(9, 0)
    end_time = time(17, 0)
    delta = timedelta(minutes=30)
    
    booked_times = Appointment.objects.filter(
        doctor=doctor,
        date__date=check_date
    ).exclude(status__name="Cancelled").values_list('date', flat=True)
    
    booked_hours = [b.time().replace(second=0, microsecond=0) for b in booked_times]
    
    current_time = datetime.combine(check_date, start_time)
    
    while current_time.time() < end_time:
        slot_time = current_time.time()
        if slot_time not in booked_hours:
            slots.append(slot_time.strftime("%H:%M"))
        current_time += delta
        
    return slots


@login_required
def dashboard(request):
    """
    Ana Sayfa: Gelecek randevuları gösterir.
    Ayrıca ana sayfadan 'Acil Durum' butonuna basılırsa kırmızı ekranı açar.
    """
    update_past_appointments()

    if request.method == 'POST' and 'emergency_dashboard' in request.POST:
        messages.error(request, "ACİL DURUM BUTONU AKTİF EDİLDİ! Lütfen sakin olun.")

        return render(request, "appointments/appointment_form.html", {
            "form": AppointmentForm(),
            "emergency_alert": True,
            "target_date": timezone.now().date()
        })

    query = request.GET.get("q", "")
    upcoming = Appointment.objects.filter(
        user=request.user, 
        date__gte=datetime.now()
    ).exclude(status__name="Cancelled").filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(status__name__icontains=query)
    ).order_by("date")
    
    return render(request, "appointments/dashboard.html", {"upcoming": upcoming, "query": query})

@login_required
def appointment_create(request):
    all_doctors = Doctor.objects.all()
    all_specialties = Doctor.objects.values_list('speciality', flat=True).distinct().order_by('speciality')

    form = AppointmentForm(request.POST or None, request.FILES or None)
    available_slots = []
    selected_doctor = None
    target_date = timezone.now().date() + timedelta(days=1)
    
    selected_doctor_id = None 

    if request.method == 'POST':
        
        if 'emergency_mode' in request.POST:
            messages.error(request, "ACİL DURUM BUTONU AKTİF EDİLDİ!")
            return render(request, "appointments/appointment_form.html", {
                "form": form, "emergency_alert": True, "target_date": target_date
            })

        date_str = request.POST.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        if 'analyze' in request.POST:
            description = request.POST.get('description', '')
            form = AppointmentForm(request.POST, request.FILES)

            if description:
                if check_emergency(description):
                    messages.error(request, "ACİL DURUM TESPİT EDİLDİ!")
                    return render(request, "appointments/appointment_form.html", {
                        "form": form, "emergency_alert": True, "target_date": target_date
                    })
                
                suggested_specialty = get_ai_specialty(description)
                
                if suggested_specialty:
                    doctors_in_spec = Doctor.objects.filter(speciality=suggested_specialty)
                    
                    if doctors_in_spec.exists():
                        selected_doctor = doctors_in_spec.annotate(
                            num_apps=Count('appointment')
                        ).order_by('num_apps').first()
                        
                        selected_doctor_id = selected_doctor.id
                        
                        data = form.data.copy()
                        data['doctor'] = selected_doctor.id
                        form.data = data
                        
                        available_slots = get_available_slots(selected_doctor, target_date)
                        
                        messages.success(request, f"Şikayetiniz '{suggested_specialty}' ile eşleşti. En müsait doktorumuz {selected_doctor.name} sizin için seçildi.")
                    else:
                        messages.warning(request, f"'{suggested_specialty}' bölümü önerildi ancak bu bölümde kayıtlı doktor bulunamadı.")
                else:
                    messages.warning(request, "Üzgünüm, şikayetinizi net bir branşla eşleştiremedim. Lütfen manuel seçim yapın.")
            
                
            
            return render(request, "appointments/appointment_form.html", {
                "form": form, "slots": available_slots, "target_date": target_date,
                "all_doctors": all_doctors, "all_specialties": all_specialties,
                "selected_doctor_id": selected_doctor_id
            })

        
        elif 'get_manual_slots' in request.POST:
            form = AppointmentForm(request.POST, request.FILES)
            doctor_id = request.POST.get('doctor')
            
            if doctor_id:
                selected_doctor = Doctor.objects.get(id=doctor_id)
                selected_doctor_id = selected_doctor.id
                available_slots = get_available_slots(selected_doctor, target_date)
                
                return render(request, "appointments/appointment_form.html", {
                    "form": form, "slots": available_slots, "target_date": target_date,
                    "manual_mode": True,
                    "all_doctors": all_doctors, "all_specialties": all_specialties,
                    "selected_doctor_id": selected_doctor_id
                })
            else:
                messages.warning(request, "Lütfen bir doktor seçiniz.")

        
        elif 'save_appointment' in request.POST:
            slot = request.POST.get('selected_slot')
            doctor_id = request.POST.get('doctor')
            
            if slot and doctor_id:
                new_app = Appointment()
                new_app.user = request.user
                
                doctor_obj = Doctor.objects.get(id=doctor_id)
                new_app.doctor = doctor_obj
                new_app.title = f"{doctor_obj.speciality} - {doctor_obj.name}"
                new_app.description = request.POST.get('description')
                
                if request.FILES.get('document'):
                    new_app.document = request.FILES.get('document')
                
                hour, minute = map(int, slot.split(':'))
                new_app.date = datetime.combine(target_date, time(hour, minute))
                
                pending_status, _ = Status.objects.get_or_create(name="Pending")
                new_app.status = pending_status
                
                new_app.save()
                
                try:
                    subject = f"Randevu Onayı: {new_app.title}"
                    message = f"Sayın {request.user.username},\n\nRandevunuz oluşturuldu.\nTarih: {new_app.date}\nDoktor: {new_app.doctor.name}"
                    send_mail(subject, message, 'admin@medai.com', [request.user.email])
                except:
                    pass

                messages.success(request, "Randevunuz başarıyla oluşturuldu!")
                return redirect("dashboard")
            else:
                messages.error(request, "Lütfen bir saat dilimi seçiniz.")

    return render(request, "appointments/appointment_form.html", {
        "form": form,
        "target_date": target_date,
        "all_doctors": all_doctors,
        "all_specialties": all_specialties
    })

@login_required
def appointment_list(request):
    update_past_appointments()
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, "appointments/appointment_list.html", {"appointments": appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    return render(request, "appointments/appointment_detail.html", {"appointment": appointment})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, "Randevu güncellendi.")
        return redirect("dashboard")
    return render(request, "appointments/appointment_form.html", {"form": form})

@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        cancelled_status, created = Status.objects.get_or_create(name="Cancelled")
        appointment.status = cancelled_status
        appointment.save()
        
        subject = f"Randevu İptali: {appointment.title}"
        message = f"""
        Sayın {request.user.username},

        {appointment.date.strftime('%d.%m.%Y %H:%M')} tarihindeki randevunuz isteğiniz üzerine İPTAL edilmiştir.

        Sağlıklı günler dileriz.
        """
        try:
            send_mail(subject, message, 'senin_mailin@gmail.com', [request.user.email])
        except:
            pass

        messages.success(request, "Randevu başarıyla iptal edildi.")
        return redirect("dashboard")
    return render(request, "appointments/confirm_cancel.html", {"appointment": appointment})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        appointment.delete()
        return redirect("dashboard")
    return render(request, "appointments/appointment_confirm_delete.html", {"appointment": appointment})

@login_required
def appointment_history(request):
    appointments = Appointment.objects.filter(user=request.user).filter(
        Q(date__lt=timezone.now()) | Q(status__name="Cancelled")
    ).order_by("-date")
    return render(request, "appointments/history.html", {"appointments": appointments})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

@login_required
def my_reports(request):
    """
    Sadece dosya/rapor yüklenmiş randevuları listeler.
    """

    reports = Appointment.objects.filter(
        user=request.user
    ).exclude(document='').exclude(document=None).order_by('-date')
    
    return render(request, "appointments/reports.html", {"reports": reports})


def update_past_appointments():

    now = timezone.now()
      
    completed_status, _ = Status.objects.get_or_create(name="Completed")
    
    past_appointments = Appointment.objects.filter(
        date__lt=now
    ).exclude(
        status__name__in=['Cancelled', 'Completed', 'Iptal']
    )
    
    count = past_appointments.count()
    
    if count > 0:
        past_appointments.update(status=completed_status)
        print(f"Sistem: {count} adet eski randevu 'Completed' olarak güncellendi.")