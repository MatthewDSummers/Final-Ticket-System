from django.shortcuts import render, redirect
import requests 
import json
from ticket_app.models import Ticket

def charts(request):
    if request.method == 'POST':
        context = {

        }
    return render(request, 'charts.html', context)

def api(request):

    # for tick in Ticket.objects.all():
    #     arr = [tick]
    array = [5,5,5], [1, 2, 3], [4, 5, 6]
    context ={
        'array' : json.dumps(array)
    }
    return render('charts.html', context)