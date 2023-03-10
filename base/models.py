from django.db import models
import datetime


def upload_location(instance, filename):
    extension_file = filename.split('.')[-1]
    time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{time_stamp}.{extension_file}"
    return '/'.join(['images', new_filename])


class ImageUpload(models.Model):
    image = models.ImageField(upload_to=upload_location, max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image


enum_image_type = (
    ('image_chart', 'image_chart'),
    ('image_result', 'image_result'),
)


class ImageResult(models.Model):
    image = models.ImageField(upload_to=upload_location, max_length=500)
    type = models.CharField(max_length=20, choices=enum_image_type)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image
