from django.shortcuts import render, redirect
from .forms import SaidaForm


def registrar_saida(request):

    if request.method == 'POST':
        form = SaidaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sucesso')

    else:
        form = SaidaForm()

    return render(
        request,
        'saidas/registrar.html',
        {'form': form}
    )


def sucesso(request):
    return render(request, 'saidas/sucesso.html')

from .models import Saida


def listar_saidas(request):
    registros = Saida.objects.all().order_by('-data', '-horario')

    return render(
        request,
        'saidas/listar.html',
        {'registros': registros}
    )










