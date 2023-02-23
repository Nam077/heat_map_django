from rest_framework import serializers

from base import models


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageUpload
        fields = ('id', 'image', 'uploaded_at', 'created_at', 'updated_at')

