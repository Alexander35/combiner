from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notify

@login_required
def notify_all(request):
	notifies = Notify.objects.filter(to=request.user)

	return render(
            request,
            'dashboard/notification_page.html',
            { 
                'title' : 'Notification Page',
                'notifies' : notifies,          
            }
        )	