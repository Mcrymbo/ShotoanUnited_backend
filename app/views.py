from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .signals import create_whatsapp_share_link
from .models import Event

# Create your views here.
def index(request):
    return HttpResponse('This is an introduction page')

def register_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'events/register.html', {'event': event})
