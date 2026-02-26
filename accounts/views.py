from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def dashboard_view(request):
    return render(request, "accounts/dashboard.html")