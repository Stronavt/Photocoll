from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image, Album, SavedImage


@receiver(m2m_changed, sender= Image.users_like.through) 
#эта функция соединяется с Image.users_like.through, чтобы функция вызывалась только в том случае, если сигнал m2m_changed был запущен этим отправителем.
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
