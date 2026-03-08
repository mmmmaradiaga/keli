from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
]