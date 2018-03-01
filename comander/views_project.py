from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, ShareProjectToUser
from .models import Project, Worker
from django.db.models import Q

@login_required
def project_settings_add_worker(request, project_id, worker_id):

	try:
		project = Project.objects.get(pk=project_id)
		project.worker.add(worker_id)
	except Exception as exc:
		print('Cannot add worker to the project : {}'.format(exc))

	return redirect('project_settings', project_id)

@login_required
def project_settings(request, project_id):

	project = Project.objects.get(pk=project_id)
	workers_list = Worker.objects.filter(Q(user__pk=request.user.id) & ~Q(project__id=project.id))

	project_workers_list = project.worker.all()

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