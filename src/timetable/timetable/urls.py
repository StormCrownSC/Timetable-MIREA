"""timetable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from schedule.views import index_page
from django.contrib.auth import views

from django.shortcuts import render, redirect

def change_themes(request):
    if request.session.get('themes', 'dark') == 'dark':
        request.session['themes'] = 'light'
    else:
        request.session['themes'] = 'dark'
    return redirect(request.META.get('HTTP_REFERER'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schedule.urls')),
    path('accounts/', include('accounts.urls')),
    path(r'change_themes', change_themes)
]
