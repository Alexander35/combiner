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
    # path('worker/settings/<worker_id>/', views.worker_settings, name="worker_settings"),

    path('project/projects-list/', views.projects_list, name='projects_list'),
    path('project/new-project/', views.new_project, name='new_project'),
    path('project/visibility/<project_id>/', views.project_visibility, name="project_visibility"),
    path('project/share_project_to/<project_id>/', views.share_project_to, name="share_project_to"),
]