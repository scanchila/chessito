from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('about/', views.about, name='main-about'),
    path('play/', views.play, name='main-play'),
    path('game/', views.game, name='main-game'),
    path('send_invite/', views.send_invite, name='send-invite'),
    
] 