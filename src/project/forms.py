from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from datetime import date
from common.models import Client, Expert, ProjectFile

INDUSTRY_CHOICES = (
    ("MC","Management Consulting"),
    ("EN","Energy"),
    ("HI","Health care and Life Sciences"),
    ("BI","BioPharma"),
    ("ED","Education"),
    ("SE","Semiconductor"),
    ("SW","Software"),
    ("MB","Mobile Internet and Computing"),
    ("DS","Data and Storage"),
    ("VR","VR/AI/Robotics"),
    ("IT","Internet of Things"),
    ("GB","Gaming and Media"),
    ("ET","Entertainment"),
    ("TL","Transport and Logistics"),
    ("AU","Automotive"),
    ("CG","Consumer Goods"),
    ("OT","Others"),
)

EXPERTISE_CHOICES = (
    ("ST","Strategy"),
    ("BD","Business Development and Sales"),
    ("SP","Strategic Partnership"),
    ("MK","Marketing"),
    ("MT","Market Research"),
    ("OS","Operations and Supply Chain"),
    ("MA","Merger and Acquisition"),
    ("DA","Data Analytics"),
    ("SE","Software Engineering"),
    ("PJ","Project Management"),
    ("PD","Product Design and Development"),
    ("PM","Product Management"),
    ("EN","Entrepreneurship"),
    ("CC","Cloud Computing"),
    ("AD","Advertisement"),
    ("CL","Corporate Law"),
    ("CF","Corporate Finance"),
    ("AT","Accounting and Taxation"),
    ("OT","Others"),
)

DEEP_DIVE = 'D'
GENERAL_ADVISORY = 'G'

SERVICE_CHOICES = (
   (DEEP_DIVE, 'Deep dive'),
   (GENERAL_ADVISORY, 'General advisory'),
)

FIXED = 'F'
HOURLY = 'H'

RATING_CHOICES = (
    (FIXED, 'Fixed amount'),
    (HOURLY, 'Hourly rate'),
)
class ProjectForm(forms.Form):
    project_name = forms.CharField(label=_('Name'), max_length=200,
                                   widget=forms.TextInput(
                                   	    attrs={'placeholder':_('Give your engagement request a name'),
                                   	           'size':'60'}))
    project_description = forms.CharField(label=_('Description'), max_length=10000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':_('Describe what needs to be done for the engagement'),
                                                    'rows':10,
                                                    'cols':59}))
    project_expert_industry = forms.ChoiceField(label=_('Expert Industry'), choices=INDUSTRY_CHOICES, required=True)
    project_expert_expertise = forms.ChoiceField(label=_('Expert Expertise'), choices=EXPERTISE_CHOICES, required=True)
    project_expert_preference = forms.CharField(label=_('Expert Preference'), max_length=1000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':_('Describe what kind of expert do you want to work with'),
                                                    'rows':4,
                                                    'cols':59}))
    project_pub_date = forms.DateTimeField(label=_('Start Date'), input_formats=['%Y-%m-%d'],
                                           widget=forms.TextInput(
                                              attrs={'placeholder':'YYYY-mm-dd',
                                                      'size':'60',
                                                      'class': 'datepicker'
                                                      }))
    project_end_date = forms.DateTimeField(label=_('Due Date'), input_formats=['%Y-%m-%d'],
                                            widget=forms.TextInput(
                                              attrs={'placeholder':'YYYY-mm-dd',
                                                      'size':'60',
                                                      'class': 'datepicker'
                                                      }))
    project_service_type = forms.ChoiceField(
        label=mark_safe('Service Type (<a href="/how_it_works/#faq" target="_blank">FAQ</a>)'),
        choices=SERVICE_CHOICES,
        required=True
    )
    project_rate_type = forms.ChoiceField(
      label=mark_safe('Rate Type (<a href="/how_it_works/#faq" target="_blank">FAQ</a>)'),
      choices=RATING_CHOICES,
      required=True)
    project_rate = forms.DecimalField(label=_('Budget'), max_digits=8, decimal_places=2,
    	                                    widget=forms.TextInput(
                                              attrs={'placeholder':_('In dollars or hours'),
                                                     'size':'60'}))
class ProjectFileForm(ModelForm):

  class Meta:
    model = ProjectFile
    fields = ['avatar']
    labels = {
        'avatar':'',
    }