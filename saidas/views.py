from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Saida


def registrar_saida(request):
    if request.method == "POST":
        qr_code = request.POST.get("qr_code")
        motivo = request.POST.get("motivo")
        responsavel = request.POST.get("responsavel")

        print("QR CODE RECEBIDO:", qr_code)

        aluno = get_object_or_404(Aluno, qr_code=qr_code)

        print("ALUNO ENCONTRADO:", aluno)
        print("NOME:", aluno.nome)
        print("TURMA:", aluno.turma)
        print("MATRÍCULA:", aluno.matricula)

        Saida.objects.create(
            aluno=aluno,
            motivo=motivo,
            responsavel=responsavel
        )

        return render(request, "saidas/sucesso.html", {
            "aluno": aluno
        })

    return render(request, "saidas/registrar_saida.html")


def historico(request):
    saidas = Saida.objects.all().order_by('-data', '-horario')
    return render(request, 'saidas/historico.html', {'saidas': saidas})
