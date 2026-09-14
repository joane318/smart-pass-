from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    turma = models.CharField(max_length=50)
    qr_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nome} - {self.turma}"


class Saida(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    motivo = models.TextField()
    responsavel = models.CharField(max_length=100)
    data = models.DateField(auto_now_add=True)
    horario = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.aluno.nome
