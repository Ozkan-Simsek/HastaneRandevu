from django.urls import path
from . import views

urlpatterns = [
    path("hasta-paneli/", views.dashboard, name="dashboard"), 
    
    path("randevularim/", views.appointment_list, name="appointment_list"),
    path("create/", views.appointment_create, name="appointment_create"),
    path("<int:pk>/edit", views.appointment_update, name="appointment_update"),
    path("<int:pk>/delete", views.appointment_delete, name="appointment_delete"),
    path("register/", views.register_view, name="register"),
    
    path("appointments/<int:pk>/", views.appointment_detail, name="appointment_detail"),
    path("appointments/<int:pk>/cancel/", views.appointment_cancel, name="appointment_cancel"),
    
    path("history/", views.appointment_history, name="appointment_history"),
    path('raporlarim/', views.my_reports, name='my_reports'),
    
    path('randevu-guncelle/<int:pk>/<str:durum>/', views.update_appointment_status, name='update_status'),
    path('randevu/<int:appointment_id>/recete-yaz/', views.add_prescription, name='add_prescription'),
    path('randevu/<int:pk>/indir/', views.generate_pdf, name='generate_pdf')
]