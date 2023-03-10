from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from base.form import ImageUploadForm, ImageResultForm
from base.models import ImageUpload, ImageResult
from base.serializer import ImageUploadSerializer, ImageResultSerializer

# Create your views here.

rooms = [
    {
        'id': 1,
        'name': 'Room 1',
        'price': 1000,
    },
    {
        'id': 2,
        'name': 'Room 2',
        'price': 2000,

    }
]


def index(request):
    return render(request, 'base/home.html', {'rooms': rooms})


def room(request):
    return render(request, 'base/room.html', {'rooms': rooms})


def login(request):
    return render(request, 'base/login.html')


def register(request):
    return render(request, 'base/register.html')


def room_detail(request, room_id):
    room_detail_find = list(filter(lambda x: x['id'] == room_id, rooms))
    return render(request, 'base/room-detail.html', {'room': room_detail_find[0]})


def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse('Image Uploaded Successfully')
    else:
        form = ImageUploadForm()
    return render(request, 'base/upload.html', {'form': form})


def image_result_upload(request):
    if request.method == 'POST':
        form = ImageResultForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'base/upload.html', {'message': 'Image Uploaded Successfully'})
    else:
        form = ImageResultForm()
    return render(request, 'base/upload_result.html', {'form': form})


def stream(request):
    image_upload_new = ImageUpload.objects.latest('created_at')
    image_result_upload_chart = ImageResult.objects.latest('created_at')
    image_result_upload_result = ImageResult.objects.latest('created_at')
    return render(request, 'base/stream.html',
                  {'image_upload': image_upload_new, 'image_result_upload_chart': image_result_upload_chart,
                   'image_result_upload_result': image_result_upload_result})


def query(request):
    # get one image latest
    image_all = ImageUpload.objects.all().order_by('-created_at')[:1]
    return Response(ImageUploadSerializer(image_all, many=True).data, status=status.HTTP_200_OK)


class ImageResultLatestList(ListCreateAPIView):
    queryset = ImageResult.objects.all().order_by('-created_at')[:1]
    serializer_class = ImageResultSerializer

    def get(self, request, *args, **kwargs):
        image_type = self.request.query_params.get('type', None)
        if image_type == 'image_chart':
            image_result = ImageResult.objects.filter(type='image_chart').order_by('-created_at')[:1]
        elif image_type == 'image_result':
            image_result = ImageResult.objects.filter(type='image_result').order_by('-created_at')[:1]
        else:
            image_result = ImageResult.objects.all().order_by('-created_at')[:1]
        return Response(ImageResultSerializer(image_result, many=True).data, status=status.HTTP_200_OK)


def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    return Response(ImageResultSerializer(queryset, many=True).data, status=status.HTTP_200_OK)


class ImageLatestList(ListCreateAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer

    def get_queryset(self):
        image_all = ImageUpload.objects.all().order_by('-created_at')[:1]
        return image_all

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(ImageUploadSerializer(queryset, many=True).data, status=status.HTTP_200_OK)


class ImageUploadList(ListCreateAPIView):
    serializer_class = ImageUploadSerializer
    queryset = ImageUpload.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = ImageUpload.objects.all()
        return queryset


class ImageResultList(ListCreateAPIView):
    serializer_class = ImageResultSerializer
    queryset = ImageResult.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = ImageResult.objects.all()
        return queryset


class ImageUploadDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ImageUploadSerializer

    def get_queryset(self):
        queryset = ImageUpload.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
