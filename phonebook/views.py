from django.http import HttpResponse
from django.views import generic

from .models import Contact

class IndexView(generic.ListView):
    model = Contact

class DetailView(generic.DetailView):
    model = Contact