from .models import ImageUpload, ImageResult
from django import forms


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ImageResultForm(forms.ModelForm):
    class Meta:
        model = ImageResult
        fields = ['image', 'type']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
