from django.urls import path
from .views import registrar_saida, historico

urlpatterns = [
    path("saida/", registrar_saida, name="registrar_saida"),
    path("historico/", historico, name="historico"),
]