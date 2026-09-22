from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Aluno, Saida


def registrar_saida(request):
    if request.method == "POST":
        qr_code = request.POST.get("qr_code")
        motivo = request.POST.get("motivo")
        responsavel = request.POST.get("responsavel")

        print("QR CODE RECEBIDO:", qr_code)

        try:
            aluno = Aluno.objects.get(qr_code=qr_code)
        except Aluno.DoesNotExist:
            return render(request, "saidas/registrar_saida.html", {
                "erro": f"QR Code não cadastrado: {qr_code}"
            })

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
    busca = request.GET.get("busca", "")

    saidas = Saida.objects.select_related("aluno").all().order_by(
        "-data", "-horario"
    )

    if busca:
        saidas = saidas.filter(
            aluno__nome__icontains=busca
        ) | saidas.filter(
            aluno__matricula__icontains=busca
        )

    return render(request, "saidas/historico.html", {
        "saidas": saidas,
        "busca": busca,
    })


def inicio(request):
    hoje = timezone.localdate()

    total_alunos = Aluno.objects.count()
    total_saidas = Saida.objects.count()
    saidas_hoje = Saida.objects.filter(data=hoje).count()

    ultimas_saidas = Saida.objects.select_related("aluno").order_by(
        "-data", "-horario"
    )[:5]

    return render(request, "saidas/inicio.html", {
        "total_alunos": total_alunos,
        "total_saidas": total_saidas,
        "saidas_hoje": saidas_hoje,
        "ultimas_saidas": ultimas_saidas,
    })