from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, ShareProjectToUser
from .models import Project, Worker, ProjectSequenceNumber
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
def proproject_run_in_sequental_mode_stuff(worker):
	try:

		worker_initialize(
			worker, True
			)

		# worker.status='Processing'
		# worker.save()

	except Exception as exc:
		print('cannot execute a worker from project: {}'.format(exc))	

@login_required
def project_run_in_sequental_mode(request, project_id):

	project = Project.objects.get(pk=project_id)

	for worker in project.worker.all():

		worker_thread = Thread(target=proproject_run_in_sequental_mode_stuff, args=(worker,))
		worker_thread.start()


	return redirect('project_status_page', project_id)

@login_required
def project_run_in_parallel_mode(request, project_id):

	project = Project.objects.get(pk=project_id)

	for worker in project.worker.all():

		try:

			worker_initialize(
				worker
				)

			# worker.status='Processing'
			# worker.save()

		except Exception as exc:
			print('cannot execute a worker from project: {}'.format(exc))	

	return redirect('project_status_page', project_id)	

@login_required
def project_sequence_number_up(request, project_id, worker_id):
	try:
		project = Project.objects.get(pk=project_id)
		worker = Worker.objects.get(pk=worker_id)
		# project_sequence_number = 
		if ProjectSequenceNumber.objects.filter(project=project, worker=worker).exists():
			project_sequence_number = ProjectSequenceNumber.objects.get(project=project, worker=worker)
			project_sequence_number.sequence_number-=1
			if project_sequence_number.sequence_number < 0:
				project_sequence_number.sequence_number = 0

		else:
			project_sequence_number = ProjectSequenceNumber(project=project, worker=worker)	

		project_sequence_number.save()

	except Exception as exc:
		print('cant update sequence number : {}'.format(exc))	

	return redirect('project_settings', project_id)	

@login_required
def project_sequence_number_down(request, project_id, worker_id):
	try:
		project = Project.objects.get(pk=project_id)
		worker = Worker.objects.get(pk=worker_id)
		# project_sequence_number = 
		if ProjectSequenceNumber.objects.filter(project=project, worker=worker).exists():
			project_sequence_number = ProjectSequenceNumber.objects.get(project=project, worker=worker)
			project_sequence_number.sequence_number+=1
			# if project_sequence_number.sequence_number < 0:
			# 	project_sequence_number.sequence_number = 0

		else:
			project_sequence_number = ProjectSequenceNumber(project=project, worker=worker)	

		project_sequence_number.save()

	except Exception as exc:
		print('cant update sequence number : {}'.format(exc))	

	return redirect('project_settings', project_id)	


@login_required
def project_settings_add_worker(request, project_id, worker_id):

	try:
		project = Project.objects.get(pk=project_id)
		project.worker.add(worker_id)
		project.save()
		worker = Worker.objects.get(pk=worker_id)
		project_sequence_number = ProjectSequenceNumber(project=project, worker=worker)	
		project_sequence_number.save()			
		# project_sequence_number_json = 
		# worker.project_sequence_number
	except Exception as exc:
		print('Cannot add worker to the project : {}'.format(exc))

	return redirect('project_settings', project_id)

@login_required
def project_settings(request, project_id):

	project = Project.objects.get(pk=project_id)
	workers_list = Worker.objects.filter(Q(user__pk=request.user.id) & ~Q(project__id=project.id))

	project_workers_list = ProjectSequenceNumber.objects.order_by('sequence_number').filter(project=project)
	print(project_workers_list)

	# print(worker_list)

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
				share_project_to_user_form.add_error(None, exc)
				print('Error when sharing project to user: {}'.format(exc))

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
				print('Ann error occured when create new Project: {}'.format(exc))

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
	except Exception as exc:
		print('cant remove user form project : {}'.format(exc))

	return redirect('projects_list')		