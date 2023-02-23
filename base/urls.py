from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('room/', views.room, name='room'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('image_upload/', views.image_upload, name='image_upload'),
    path('api/image/latest/', views.ImageLatestList.as_view(), name='image_latest'),
    path('api/image/', views.ImageUploadList.as_view(), name='image_upload_list'),
    path('api/image/<int:pk>/', views.ImageUploadDetail.as_view(), name='image_upload_detail'),
]
