from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, ShareProjectToUser
from .models import Project, Worker, Notify
from django.db.models import Q
from .worker_suite import worker_initialize
from threading import Thread
import json

@login_required
def project_status_page(request, project_id):

	project = Project.objects.get(pk=project_id)

	return render(
            request,
            'project/project_status_page.html',
            { 
                'title' : 'Project Status Page',
                'project' : project,          
            }
        )
def worker_priotity_divide(worker_list):

	data_miner = [worker for worker in worker_list if worker.priority == 'data_miner']
	processor = [worker for worker in worker_list if worker.priority == 'processor']	
	harvester = [worker for worker in worker_list if worker.priority == 'harvester']

	return [data_miner, processor, harvester]

def proproject_run_in_sequental_mode_stuff(worker):
	try:

		worker_initialize(
			worker,True
			)

	except Exception as exc:
		notify = Notify(notify_type='error', data='cannot execute a worker from project: {}'.format(exc))
		notify.save()	

@login_required
def project_run_in_sequental_mode(request, project_id):

	project = Project.objects.get(pk=project_id)

	[data_miner, processor, harvester] = worker_priotity_divide(project.worker.all())

	for worker in data_miner:
		worker_thread = Thread(target=proproject_run_in_sequental_mode_stuff, args=(worker,))
		worker_thread.start()

	for worker in processor:
		worker_thread = Thread(target=proproject_run_in_sequental_mode_stuff, args=(worker,))
		worker_thread.start()

	for worker in harvester:
		worker_thread = Thread(target=proproject_run_in_sequental_mode_stuff, args=(worker,))
		worker_thread.start()


	return redirect('project_status_page', project_id)

@login_required
def project_run_in_parallel_mode(request, project_id):

	try:
		project = Project.objects.get(pk=project_id)

		[data_miner, processor, harvester] = worker_priotity_divide(project.worker.all())	

		for worker in data_miner:
			Thread(target=worker_initialize, args=(worker,)).start()
		for worker in processor:
			Thread(target=worker_initialize, args=(worker,)).start()
		for worker in harvester:
			Thread(target=worker_initialize, args=(worker,)).start()						
		# [worker_initialize(worker, request.user) for worker in data_miner]
		# [worker_initialize(worker, request.user) for worker in processor]	
		# [worker_initialize(worker, request.user) for worker in harvester]
	except Exception as exc:
		notify = Notify(notify_type='error', data='cannot execute project in parallel mode : {}'.format(exc), to=request.user)
		notify.save()			

	return redirect('project_status_page', project_id)	

@login_required
def project_settings_add_worker(request, project_id, worker_id):

	try:
		project = Project.objects.get(pk=project_id)
		project.worker.add(worker_id)
		project.save()
		worker = Worker.objects.get(pk=worker_id)
	except Exception as exc:
		notify = Notify(notify_type='error', data='Cannot add worker to the project : {}'.format(exc), to=request.user)
		notify.save()

	return redirect('project_settings', project_id)

@login_required
def project_settings(request, project_id):

	project = Project.objects.get(pk=project_id)
	workers_list = Worker.objects.filter(Q(user__pk=request.user.id) & ~Q(project__id=project.id))

	project_workers_list = Worker.objects.filter(project__id=project_id)

	return render(
            request,
            'project/project_settings.html',
            { 
                'title' : 'Project Settings',
                'project' : project,  
                'workers_list' : workers_list,
                'project_workers_list' : project_workers_list,           
            }
        ) 

@login_required
def share_project_to(request, project_id):
	share_project_to_user_form = ShareProjectToUser()

	if request.method == 'POST':
		share_project_to_user_form = ShareProjectToUser(request.POST)
		if share_project_to_user_form.is_valid():
			print(request.POST['share_to'])
			try:	
				user = User.objects.get(pk=request.POST['share_to'])
				project = Project.objects.get(pk=project_id)
				project.user.add(user)
				project.save()
			except Exception as exc:
				notify = Notify(notify_type='error', data='Error when sharing project to user: {}'.format(exc), to=request.user)
				notify.save()
				share_project_to_user_form.add_error(None, exc)

	return redirect('projects_list')	

@login_required
def projects_list(request):

	projects_list = Project.objects.filter(user__id=request.user.id)
	share_project_to_user_form = ShareProjectToUser()

	return render(
            request,
            'project/projects_list.html',
            { 
                'title' : 'Project List',
                'projects_list' : projects_list,   
                'share_project_to_user_form' : share_project_to_user_form,              
            }
        )     


@login_required
def new_project(request):

	add_project_form = AddProjectForm()

	if request.method == 'POST':
		add_project_form = AddProjectForm(request.POST)
		if add_project_form.is_valid():
			try:
				project = Project(
        			name=request.POST['name'],
        			description=request.POST['description'],
        			)
				project.save()
				project.user.add(request.user.id)
				project.save()
				return redirect('projects_list')
			except Exception as exc:
				add_project_form.add_error(None, exc)
				notify = Notify(notify_type='error', data='Ann error occured when create new Project: {}'.format(exc), to=request.user)
				notify.save()

	return render(
            request,
            'project/new_project.html',
            { 
                'title' : 'New Project', 
                'add_project_form' : add_project_form,
            }
        ) 

@login_required
def project_visibility(request, project_id):
	try:
		project = Project.objects.get(pk=project_id)
		project.user.remove(request.user)
		project.save()
	except Exception as exc:
		notify = Notify(notify_type='error', data='cant remove user form project : {} {}'.format(project.name, exc), to=request.user)
		notify.save()		

	return redirect('projects_list')		