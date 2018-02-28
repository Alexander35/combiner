from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddWorkerForm, ShareWorkerToUser
from .models import Worker
from .views_worker import *
from .views_project import *

# Create your views here.

@login_required
def dashboard(request, action=''):
    return render(
            request,
            'dashboard/main.html',
            { 
                'title' : 'Dashboard',                
            }
        )