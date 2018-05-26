import datetime

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import UserForm, bandForm, DocumentForm, UserCreationForm
from .models import Event, ContestCalendar, searchBandSugg, Document
from calendar import monthrange
from operator import and_
from django.db.models import Q
from functools import reduce

# Create your views here.
def home(request):
    return render(request, 'front/base.html')