from django.contrib.auth import views
from django.urls import path

from .views import *

urlpatterns = [
    path('', index_page, name='home'),
    path('timetable/', timetable_page, name='timetable'),
    path('timetable/change_type_info/', change_type_info, name='change_type_info')
]