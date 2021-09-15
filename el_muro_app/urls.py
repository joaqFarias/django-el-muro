from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('nuevo/<str:tipo_texto>', views.nuevo_mensaje_comentario),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
]
