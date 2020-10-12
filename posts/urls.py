
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [

    path('timeline/',views.ImagePostView.as_view(),name='timeline'),
    path('image-upload/',views.ImageFormView.as_view(), name = 'image_upload')
]