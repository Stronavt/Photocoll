import datetime
from django.contrib.contenttypes.models import ContentType
from .models import Action
from django.utils import timezone


def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        print('target_ct: ', target_ct, 'target: ', target)
        #CT - содержит всю информацию о моделях в проекте. target-экземпляр модели
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)
        #фильтр чтобы выбрать только те действия, которые связаны с конкретной целью(target_ct-тип контента, id-его индификатор)
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False

#Ищет все действия, связанные с определенным пользователем, определенным глаголом и созданные за последнюю минуту.
#Если задан объект target, он дополнительно фильтрует действия по типу и идентификатору этого объекта.
#Если не найдено похожих действий, создается новое действие с указанными параметрами и сохраняется в базе данных.