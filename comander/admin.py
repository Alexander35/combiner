from django.contrib import admin

# Register your models here.
from .models import Worker, Data, Project, ProjectSequenceNumber

admin.site.register(Worker)
admin.site.register(Data)
admin.site.register(Project)
admin.site.register(ProjectSequenceNumber)
