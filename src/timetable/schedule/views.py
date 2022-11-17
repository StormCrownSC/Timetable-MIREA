from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')

# Create your views here.
