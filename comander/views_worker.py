from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddWorkerForm, ShareWorkerToUser
from .models import Worker, Data, Notify, Worker_Msg
from .worker_suite import worker_initialize

@login_required
def run_worker(request, worker_id):
	worker = Worker.objects.get(pk=worker_id)
	try:
		worker_initialize(
			worker, request.user
			)
	except Exception as exc:
		notify = Notify(notify_type='error', data='Cannot execute a worker : {} {}'.format(worker.name, exc), to=request.user)
		notify.save()

	return redirect('worker_status_page', worker.id)

@login_required
def worker_status_page(request, worker_id):	
	worker = Worker.objects.get(pk=worker_id)

	worker_data_history = Data.objects.order_by('-created_at').filter(from_worker_id=worker) 
	worker_logs = Worker_Msg.objects.order_by('-created_at').filter(worker=worker)

	return render(
            request,
            'worker/worker_status_page.html',
            { 
                'title' : 'Worker Status Page',
                'worker' : worker,   
                'worker_data_history' : worker_data_history,   
                'worker_logs' : worker_logs,        
            }
        )  

@login_required
def share_worker_to(request, worker_id):
	share_worker_to_user_form = ShareWorkerToUser()

	if request.method == 'POST':
		share_worker_to_user_form = ShareWorkerToUser(request.POST)
		if share_worker_to_user_form.is_valid():
			print(request.POST['share_to'])
			try:	
				user = User.objects.get(pk=request.POST['share_to'])
				worker = Worker.objects.get(pk=worker_id)
				worker.user.add(user)
				worker.save()
			except Exception as exc:
				share_worker_to_user_form.add_error(None, exc)
				notify = Notify(notify_type='error', data='Error when sharing worker to user: {}'.format(exc), to=request.user)
				notify.save()

	return redirect('workers_list')	

@login_required
def workers_list(request):

	workers_list = Worker.objects.filter(user__id=request.user.id)
	share_worker_to_user_form = ShareWorkerToUser()

	return render(
            request,
            'worker/workers_list.html',
            { 
                'title' : 'Worker List',
                'workers_list' : workers_list,   
                'share_worker_to_user_form' : share_worker_to_user_form,              
            }
        )     

@login_required
def new_worker(request):

	add_worker_form = AddWorkerForm()

	if request.method == 'POST':
		add_worker_form = AddWorkerForm(request.POST)
		if add_worker_form.is_valid():
			try:
				worker = Worker(
        			name=request.POST['name'],
        			description=request.POST['description'],
        			input_params=request.POST['input_params'],
        			run_command=request.POST['run_command'],
        			priority=request.POST['priority'],
        			char_set=request.POST['char_set'],
        			str_error_type=request.POST['str_error_type'],
        			)
				worker.save()
				worker.user.add(request.user.id)
				worker.save()
				return redirect('workers_list')
			except Exception as exc:
				add_worker_form.add_error(None, exc)
				notify = Notify(notify_type='error', data='Ann error occured when create new Worker: {}'.format(exc), to=request.user)
				notify.save()				

	return render(
            request,
            'worker/new_worker.html',
            { 
                'title' : 'New Worker', 
                'add_worker_form' : add_worker_form,
            }
        )     

@login_required
def worker_visibility(request, worker_id):
	try:
		worker = Worker.objects.get(pk=worker_id)
		worker.user.remove(request.user)
	except Exception as exc:
		notify = Notify(notify_type='error', data='cant remove user form worker : {}'.format(exc), to=request.user)
		notify.save()

	return redirect('workers_list')	