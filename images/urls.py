from . import views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

app_name = 'images'

urlpatterns = [

    path('create_form/', views.image_create_form, name='create-image-form'),
    path('update_form/<int:image_id>', views.image_update_form, name='update-image-form'),
    path('detail/<int:id>/<slug:slug>/',views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('image/tag/<slug:tag_slug>/', views.image_list, name='image_list_by_tag'),

    path('', views.image_list, name='list'),
    path('delete/<int:id>/<slug:slug>/', views.image_delete, name='image-delete'),
    
    path('save_to_album/<int:image_id>/<int:album_id>/', views.add_image_to_album, name='save_to_album'),
    path('add_image_to_album/<int:image_id>/', views.add_image_to_album, name='add_image_to_album'),
    path('remove_image_from_album/<int:image_id>/<int:album_id>/', views.remove_image_from_album, name='remove_image_from_album'),

    path('album_detail/<int:album_id>/<slug:album_slug>/', views.album_detail, name='album_detail'),
    path('create_album/', views.create_album, name='create_album'),

    path('comment/<int:image_id>/', views.add_comment, name='add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)