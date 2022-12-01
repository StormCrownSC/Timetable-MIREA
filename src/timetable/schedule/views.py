from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index_page(request):
    return render(request, 'index.html')

@login_required
def timetable_page(request):
    return render(request, "timetable.html")
