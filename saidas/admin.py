from django.contrib import admin
from .models import Aluno, Saida


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma')
    search_fields = ('nome', 'matricula', 'turma')


@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'motivo', 'data', 'horario')
    search_fields = ('aluno__nome', 'aluno__matricula')
    list_filter = ('data',)
