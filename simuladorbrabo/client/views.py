import requests
from django.shortcuts import render

# Create your views here.

def teams(request):
    aux = requests.get('http://localhost:8000/api/teams/')
    times = aux.json()
    return render(request, 'teams.html', {'times': times})

