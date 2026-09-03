from django.db import models


class Saida(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.CharField(max_length=50)
    motivo = models.TextField()
    data = models.DateField(auto_now_add=True)
    horario = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
