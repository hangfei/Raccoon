from django import forms
from django.utils.safestring import mark_safe

from datetime import date
from common.models import Client, Expert

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
    project_name = forms.CharField(label='Name', max_length=200,
                                   widget=forms.TextInput(
                                   	    attrs={'placeholder':'Give your project a name',
                                   	           'size':'60'}))
    project_description = forms.CharField(label='Description', max_length=10000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':'Describe what needs to be done for the project',
                                                    'rows':10,
                                                    'cols':59}))
    project_expert_industry = forms.ChoiceField(label='Expert Industry', choices=INDUSTRY_CHOICES, required=True)
    project_expert_expertise = forms.ChoiceField(label='Expert Expertise', choices=EXPERTISE_CHOICES, required=True)
    project_expert_preference = forms.CharField(label='Expert Preference', max_length=1000,
                                           widget=forms.Textarea(
                                   	         attrs={'placeholder':'Tell us what kind of expert do you want to work with',
                                                    'rows':4,
                                                    'cols':59}))
    project_pub_date = forms.DateTimeField(label='Start Date', input_formats=['%Y-%m-%d'],
                                           widget=forms.TextInput(
                                              attrs={'placeholder':'YYYY-mm-dd',
                                                      'size':'60',
                                                      'class': 'datepicker'
                                                      }))
    project_end_date = forms.DateTimeField(label='Due Date', input_formats=['%Y-%m-%d'],
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
    project_rate = forms.DecimalField(label='Budget', max_digits=8, decimal_places=2,
    	                                    widget=forms.TextInput(
                                              attrs={'placeholder':'In dollars or hours',
                                                     'size':'60'}))