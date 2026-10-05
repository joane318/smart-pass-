from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count
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

        hoje = timezone.localdate()

        if Saida.objects.filter(aluno=aluno, data=hoje).exists():
            return render(request, "saidas/registrar_saida.html", {
                "erro": f"O aluno {aluno.nome} já teve uma saída registrada hoje."
            })

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
def alunos(request):
    alunos = Aluno.objects.all().order_by("turma", "nome")

    return render(request, "saidas/alunos.html", {
        "alunos": alunos,
    })
def cadastrar_aluno(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        matricula = request.POST.get("matricula")
        turma = request.POST.get("turma")
        qr_code = request.POST.get("qr_code")

        Aluno.objects.create(
            nome=nome,
            matricula=matricula,
            turma=turma,
            qr_code=qr_code
        )

        return redirect("alunos")

    return render(request, "saidas/cadastrar_aluno.html")

def diagnostico(request):
    import calendar
    from datetime import date
    from django.db.models import Count

    hoje = timezone.localdate()

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    nome_mes = meses[hoje.month - 1]

    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]

    saidas_por_dia = (
        Saida.objects
        .filter(
            data__year=hoje.year,
            data__month=hoje.month
        )
        .values("data")
        .annotate(total=Count("id"))
        .order_by("data")
    )

    dados = []

    for dia in range(1, ultimo_dia + 1):

        data_dia = date(hoje.year, hoje.month, dia)

        quantidade = 0

        for item in saidas_por_dia:
            if item["data"] == data_dia:
                quantidade = item["total"]
                break

        dados.append({
            "dia": dia,
            "quantidade": quantidade
        })

    maior_quantidade = max(
        [item["quantidade"] for item in dados],
        default=1
    )

    total_saidas = Saida.objects.filter(
        data__year=hoje.year,
        data__month=hoje.month
    ).count()

    motivos = (
        Saida.objects
        .filter(
            data__year=hoje.year,
            data__month=hoje.month
        )
        .values("motivo")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    
    dados_motivos = []

    for item in motivos:

        if total_saidas > 0:
            porcentagem = round(
                (item["total"] / total_saidas) * 100,
                1
            )
        else:
            porcentagem = 0

        saidas_do_motivo = Saida.objects.filter(
            data__year=hoje.year,
            data__month=hoje.month,
            motivo=item["motivo"]
        ).select_related("aluno")

        dados_motivos.append({
            "motivo": item["motivo"],
            "total": item["total"],
            "porcentagem": porcentagem,
            "alunos": saidas_do_motivo
        })

    return render(request, "saidas/diagnostico.html", {
        "dados": dados,
        "mes": f"{nome_mes} de {hoje.year}",
        "maior_quantidade": maior_quantidade,
        "motivos": dados_motivos,
        "total_saidas": total_saidas,
    })
@require_POST
def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id)
    saida.delete()

    return redirect("inicio")















































