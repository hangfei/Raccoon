from django.shortcuts import render
from upload.forms import ImageForm
# Create your views here.
def index(request):
    if request.method == 'POST':
      new_image = ImageForm(request.POST)
      if(new_image.is_valid()):
        print(new_image.save())
      form = ImageForm(label_suffix=' ')
      return render(request, 'index.html', {'form':form})
    else:
      form = ImageForm(label_suffix=' ')
      return render(request, 'index.html', {'form':form})