from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from appointments import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.landing_page, name='landing_page'),

    path('yonlendir/', views.login_success_redirect, name='login_redirect'),
    path('doktor-paneli/', views.doctor_panel, name='doctor_panel'),
    path('', include("appointments.urls")), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)