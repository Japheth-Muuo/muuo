from django.urls import path, include
from . import views
from .views import CustomLoginView 
urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the home route
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-dosage/', views.add_dosage, name='add_dosage'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs

]
