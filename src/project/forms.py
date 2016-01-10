from django import forms
from datetime import date
class ProjectForm(forms.Form):
    project_name = forms.CharField(label='Name', max_length=200,
                                   widget=forms.TextInput(
                                   	    attrs={'placeholder':'Give your project a name',
                                   	           'size':'42'}))
    project_description = forms.CharField(label='Description', max_length=10000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':'Describe what needs to be done for the project'}))
    project_expert_preference = forms.CharField(label='Expert Preference', max_length=1000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':'Tell us what kind of expert do you want to work with'}))
    project_pub_date = forms.DateTimeField(label='Start Date', input_formats=['%Y-%m-%d'],
                                           widget=forms.TextInput(
                                              attrs={'placeholder':'YYYY-mm-dd',
                                                      'size':'42'}))
    project_end_date = forms.DateTimeField(label='Due Date', input_formats=['%Y-%m-%d'],
                                            widget=forms.TextInput(
                                              attrs={'placeholder':'YYYY-mm-dd',
                                                      'size':'42'}))
    project_rate = forms.DecimalField(label='Budget', max_digits=6, decimal_places=2,
    	                                    widget=forms.TextInput(
                                              attrs={'placeholder':'In dollars',
                                                     'size':'42'}))