from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	path('', RedirectView.as_view(url='dashboard/main/')),
    path('dashboard/<action>/', views.dashboard, name='dashboard'),
   
    path('worker/workers-list/', views.workers_list, name='workers_list'),
    path('worker/new-worker/', views.new_worker, name='new_worker'),
    path('worker/visibility/<worker_id>/', views.worker_visibility, name="worker_visibility"),
    path('worker/share_worker_to/<worker_id>/', views.share_worker_to, name="share_worker_to"),
	path('worker/run/<worker_id>/', views.run_worker, name="run_worker"),
    path('worker/status_page/<worker_id>/', views.worker_status_page, name="worker_status_page"),

    path('project/projects-list/', views.projects_list, name='projects_list'),
    path('project/new-project/', views.new_project, name='new_project'),
    path('project/visibility/<project_id>/', views.project_visibility, name="project_visibility"),
    path('project/share_project_to/<project_id>/', views.share_project_to, name="share_project_to"),
    path('project/settings/<project_id>/', views.project_settings, name="project_settings"),
    path('project/settings/add-worker/<project_id>/<worker_id>/', views.project_settings_add_worker, name="project_settings_add_worker"),
    path('project/run_in_sequental_mode/<project_id>/', views.project_run_in_sequental_mode, name="project_run_in_sequental_mode"), 
    path('project/run_in_parallel_mode/<project_id>/', views.project_run_in_parallel_mode, name="project_run_in_parallel_mode"),  
    path('project/status_page/<project_id>/', views.project_status_page, name="project_status_page"),   

    path('notify/all/', views.notify_all, name="notify_all"),
      
]