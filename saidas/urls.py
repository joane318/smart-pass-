from django.urls import path

from . import views

urlpatterns = [

    path("", views.inicio, name="inicio"),

    path("saida/", views.registrar_saida, name="registrar_saida"),

    path("historico/", views.historico, name="historico"),

    path("alunos/", views.alunos, name="alunos"),

]