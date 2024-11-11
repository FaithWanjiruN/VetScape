from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page view
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/nearby/', views.nearby_clinics, name='nearby_clinics'),
     path('form/', views.form, name='form'),
]
