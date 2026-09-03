from django.urls import path
from . import views


urlpatterns = [
    path('', views.registrar_saida, name='registrar'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('registros/', views.listar_saidas, name='registros'),
]