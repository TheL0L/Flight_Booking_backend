from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def Booking(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())
