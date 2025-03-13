from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def gear_index(request):
    return render(request, 'gear/gear-index.html')


