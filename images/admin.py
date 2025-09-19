from django.contrib import admin
from .models import Image, Album, SavedImage, Comment


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', 'id']
    list_filter = ['created']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'id', 'user']
    list_filter = ['created']

@admin.register(SavedImage)
class SavedImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'album']
    list_filter = ['saved_at']


@admin.register(Comment)
class SavedImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    list_filter = ['created']    