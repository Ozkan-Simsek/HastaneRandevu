from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from appointments import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"), 
    path("randevularim/", views.appointment_list, name="appointment_list"),
    path("create/", views.appointment_create, name="appointment_create"),
    path("<int:pk>/edit", views.appointment_update, name="appointment_update"),
    path("<int:pk>/delete", views.appointment_delete, name="appointment_delete"),
    path("register/", views.register_view, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("appointments/<int:pk>/", views.appointment_detail, name="appointment_detail"),
    path("appointments/<int:pk>/cancel/", views.appointment_cancel, name="appointment_cancel"),
    path("history/", views.appointment_history, name="appointment_history"),
    path('raporlarim/', views.my_reports, name='my_reports'),
]