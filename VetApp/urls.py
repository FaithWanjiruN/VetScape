from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),  # Home page view
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('clinics/', views.clinic_list, name='clinic_list'),  # Clinics page
    path('clinics/nearby/', views.nearby_clinics, name='nearby_clinics'),  # Nearby clinics
    path('send-adoption-email/', views.send_adoption_email, name='send_adoption_email'),
]