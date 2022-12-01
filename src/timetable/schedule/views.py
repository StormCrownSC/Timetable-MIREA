from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')

def timetable_page(request):
    return render(request, "timetable.html")
