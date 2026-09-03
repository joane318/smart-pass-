from django.contrib import admin
from .models import Saida


@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'turma',
        'motivo',
        'data',
        'horario',
    )

    search_fields = (
        'nome',
        'turma',
    )

    list_filter = (
        'turma',
        'data',
    )
