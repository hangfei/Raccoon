from django import forms
from common.models import Image

# Create your models here.
class ImageForm(forms.ModelForm):

	class Meta:
		model = Image
		fields = '__all__'