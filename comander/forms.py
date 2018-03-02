from django import forms
from django.contrib.auth.models import User
from .models import Worker
# from django.forms import ModelForm

class ShareWorkerToUser(forms.Form):
	share_to = forms.ModelChoiceField(
			queryset=User.objects.all(), 
			empty_label="/No One/"
		)

class ShareProjectToUser(forms.Form):
	share_to = forms.ModelChoiceField(
			queryset=User.objects.all(), 
			empty_label="/No One/"
		)	

# class AddWorkerToProject(forms.Form):
    
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)

    
#     info = forms.ModelChoiceField(
#             queryset=Worker.objects.filter(user=self.user), 
#             empty_label="/No One/"
#         )


class AddProjectForm(forms.Form):
	name = forms.CharField(
		widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Project Name',
                'type': 'text',
            }))
	description = forms.CharField(
		widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Project Description',
                'type': 'text',
            }))	

class AddWorkerForm(forms.ModelForm):   
    class Meta:
        model = Worker
        fields = (
            'name',
            'description',
            'input_params',
            'run_command',
            'char_set',
            'str_error_type',
        )
        widgets= {
            'name': forms.TextInput(attrs={'placeholder': 'Worker Name'}),
            'description': forms.TextInput(attrs={'placeholder': 'Worker Description'}),
            'input_params': forms.TextInput(attrs={'placeholder': 'Input Params "p1, p2, ..."'}),
            'run_command': forms.TextInput(attrs={'placeholder': 'Run Command'}),
        }

# class AddWorkerForm(forms.Form):

#     CAHRSET = (
#         ('cp886','cp886'),
#         ('cp1251','cp1251'),
#         ('utf-8','utf-8'),
#         ('latin-1','latin-1'),
#         ('ascii','ascii'),
#         ('koi8-r','koi8-r'),
#         )

#     STRENCODEERRORTYPE = (
#         ('strict','strict'),
#         ('ignore','ignore'),
#         ('replace','replace'),
#         ('xmlcharrefreplace','xmlcharrefreplace'),
#         ('backslashreplace','backslashreplace'),
#         )
        

#     chat_set = forms.ModelChoiceField(
#             queryset= 
#         )

#     name = forms.CharField(
# 		widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Worker Name',
#                 'type': 'text',

#             }))

#     input_params = forms.CharField(
# 		widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Input Params "p1, p2, ..." ',
#                 'type': 'text',

#             }))

#     run_command = forms.CharField(
# 		widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Run Command',
#                 'type': 'text',

#             }))