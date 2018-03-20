from django import forms
from django.contrib.auth.models import User
from .models import Worker

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
            'path',
            'input_params',
            'run_command',
            'command_type',
            'priority',
            'char_set',
            'str_error_type',
        )
        widgets= {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Worker Name',
                    'class': 'form-control', 
                    }
                ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Worker Description',
                    'class': 'form-control',
                    }
                ),
            'path': forms.TextInput(
                attrs={
                    'placeholder': 'Absolute Path',
                    'class': 'form-control',
                    'required' : False,
                    }
                ),            
            'input_params': forms.TextInput(
                attrs={
                    'placeholder': 'Input Params "p1, p2, ..."',
                    'class': 'form-control',
                    }
                ),
            'run_command': forms.TextInput(
                attrs={
                    'placeholder': 'Run Command',
                    'class': 'form-control',
                    }
                ),
            'command_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                ),            
            'priority': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                ),            
            'char_set': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                ), 
            'str_error_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                ),                            
        }