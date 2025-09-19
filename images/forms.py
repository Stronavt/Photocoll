from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests
from django import forms
from .models import Image, Album, Comment
from taggit.models import Tag


class ImageCreateForm(forms.ModelForm):
    albums = forms.ModelMultipleChoiceField(
        queryset=Album.objects.none(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple 
    )

    class Meta:
        model = Image
        fields = ['title', 'image', 'tags']
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['albums'].queryset = Album.objects.filter(user=user)

    def save(self, commit=True):
        image_instance = super().save(commit=commit)
        if commit:
            image_instance.albums.set(self.cleaned_data['albums'])
        return image_instance    
            
class AddImageToAlbumForm(forms.Form):
    albums = forms.ModelMultipleChoiceField(
        queryset=Album.objects.none(),
        required=True,
        widget=forms.CheckboxSelectMultiple  # или SelectMultiple
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['albums'].queryset = Album.objects.filter(user=user)
           


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment           
        fields = ['body']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']        
