from django import forms
from datetime import date
from common.models import Client, Expert

INFORMATION_TECHNOLOGY = 'IT'
MOBILE_INTERNET = 'MB'
SOFTWARE_AND_DATABASE_SYSTEMS = 'SW'
HARDWARE_AND_STORAGE = 'HW'
BIOTECH = 'BI'
LIFE_SCIENCES = 'LS'
CONSULTING_SERVICES = 'CS'
POWER_AND_ENERGY = 'PE'
OTHERS = 'OT'

INDUSTRY_CHOICES = (
   (INFORMATION_TECHNOLOGY, 'Information Technology'),
   (MOBILE_INTERNET, 'Mobile Internet'),
   (SOFTWARE_AND_DATABASE_SYSTEMS, 'Software and Database System'),
   (HARDWARE_AND_STORAGE, 'Hardware and Storage'),
   (BIOTECH, 'Biotech'),
   (LIFE_SCIENCES, 'Life Science'),
   (CONSULTING_SERVICES, 'Consulting Services'),
   (POWER_AND_ENERGY, 'Power and Energy'),
   (OTHERS, 'Others'),
)

MANAGEMENT_CONSULTING = 'MC'
ENTREPRENEURSHIP = 'EN'
CORPORATE_STRATEGY = 'CS'
BUSINESS_DEVELOPMENT = 'BD'
PRODUCT_MANAGEMENT = 'PM'
MERGER_ACQUISITION = 'MA'
SALES_MARKETING = 'SM'
LEGAL_SERVICES = 'LS'
FINANCE_ACCOUNTING = 'FA'
OTHERS = 'OT'

EXPERTISE_CHOICES = (
   (MANAGEMENT_CONSULTING, 'Management Consulting'),
   (ENTREPRENEURSHIP, 'Entrepreneurship'),
   (CORPORATE_STRATEGY, 'Corporate Strategy'),
   (BUSINESS_DEVELOPMENT, 'Business Development'),
   (PRODUCT_MANAGEMENT, 'Product Management'),
   (MERGER_ACQUISITION, 'Merger and Acquisition'),
   (SALES_MARKETING, 'Sales and Marketing'),
   (LEGAL_SERVICES, 'Legal Services'),
   (FINANCE_ACCOUNTING, 'Finance and Accounting'),
   (OTHERS, 'Others'),
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
    project_service_type = forms.ChoiceField(label='Service Type', choices=SERVICE_CHOICES, required=True)
    project_rate_type = forms.ChoiceField(label='Rate Type', choices=RATING_CHOICES, required=True)
    project_rate = forms.DecimalField(label='Budget', max_digits=6, decimal_places=2,
    	                                    widget=forms.TextInput(
                                              attrs={'placeholder':'In dollars or hours',
                                                     'size':'60'}))