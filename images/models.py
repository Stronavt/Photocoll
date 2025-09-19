from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager





class Image(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=2000, blank=True)
    #url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    #album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])



class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # images не использовать, тк связь идет через SavedImage
    images = models.ManyToManyField(Image, related_name='in_albums', blank=True)

    class Meta:
        ordering = ['-created']
        unique_together = ['user', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class SavedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_images')
    image = models.ForeignKey(Image, on_delete = models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    # Эта запись о сохранении привязана к ОДНОМУ альбому пользователя
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='saved_items')

    class Meta:
        unique_together = ['user', 'image', 'album']


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    #для анонимных пользователей
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.image}"
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]