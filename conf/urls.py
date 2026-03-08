from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# simple redirect to login
def home_redirect(request):
    return redirect('authentication:login')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_redirect), 
    path("", include("authentication.urls")),
    path("", include("profiles.urls")),
]