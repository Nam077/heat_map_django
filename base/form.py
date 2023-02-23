from .models import ImageUpload
from django import forms


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields =  ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
