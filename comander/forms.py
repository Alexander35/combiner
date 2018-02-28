from django import forms
from django.contrib.auth.models import User

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

class AddWorkerForm(forms.Form):
	name = forms.CharField(
		widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Worker Name',
                'type': 'text',

            }))
	input_params = forms.CharField(
				widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input Params "p1, p2, ..." ',
                'type': 'text',

            }))
	run_command = forms.CharField(
				widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Run Command',
                'type': 'text',

            }))