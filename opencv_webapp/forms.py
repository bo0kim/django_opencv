from django import forms
from .models import ImageUploadModel

# class naming
# SimpleUploadForm : PascalCase
# simpleUploadForm : camelCase
# simple_upload_form : snake_case

class SimpleUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('description', 'document')
