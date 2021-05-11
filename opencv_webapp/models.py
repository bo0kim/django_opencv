from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to='images/%Y/%m/%d') # forms.ImageField와 같음
    uploaded_at = models.DateTimeField(auto_now_add=True)
