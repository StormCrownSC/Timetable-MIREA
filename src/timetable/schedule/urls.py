from django.contrib.auth import views
from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='home'),
    path('timetable/', timetable_page, name='timetable'),
]