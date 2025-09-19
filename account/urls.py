from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

#app_name = 'account'


urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    #path('profile/', views.profile_page, name='profile_page'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    #user_follow обязательно над user_detail
    path('users/<username>/', views.user_detail, name='user_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
