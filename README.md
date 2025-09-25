Photocoll - социальная платформа для обмена изображениями. Пользователи могут создавать профили, подписывать под профилями других пользователей, загружать фото с тегами и заголовками, лайкать/комментировать/сохранять изображения других пользователей, также видеть действия пользователей, на которых осуществлена подписка. Проект построен на Django c FBV. 

Основные функции
Account:
-  регистрация/логин пользователей, редактирование профиля, список пользователя,  детальные страницы пользователей, подписка. Страничка dashboard с последними действия от подписок + изображения пользователей

Actions: логирование событий(like, save) с GenericForeignKey. в utils.py приведен код создания действий без дубликатов.

Images:
- загрузка, удаление , обновление изображений с тегами, используя Taggit. В представлении приведен код добавления лайков, комментариев под изображениями,сохранение изображений в альбомы и их удаление из альбомов, также добавление альбомов

Инструменты: 
- social-django, миниатюры (easy-thumbnails), debug-toolbar (откладка)

Технологии:
- Backend : Django 4.2, Python 3.8+
- Database : SQLite
- Дополнительно: Pillow, Taggit, Social-auth(OAuth), Easy-thumbnails, Django-extensions
- Frontend: JS, Bootstrap

Установка 
1. клонирование репозитория: git clone https://github.com/Stronavt/Photocoll.git 
2. python3 -m venv venv
3. source venv/bin/activate
4. pip3 install -r requirements.txt
5. обновите SECRET_KEY, DATABASE_URL
6. python3 manage.py makemigrations && python3 manage.py migrate
7. python3 manage.py createsuperuser
8. python3 manage.py runserver
9. основная страница : http://127.0.0.1:8000/account/ или http://127.0.0.1:8000/images/
10. сайт админа : http://127.0.0.1:8000/admin/
