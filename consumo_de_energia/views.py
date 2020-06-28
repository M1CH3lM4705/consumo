from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import AparelhoForm, AmbienteForm, AppForm, InsertAppForm
from django.contrib import messages
from .models import Aparelho, Ambiente
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalDeleteView,
                                           BSModalReadView)

# Create your views here.


#função que cadastra o aparalho
def save_aparelho(request):
    template_name = 'save_aparelho.html'
    context = {}
    if request.method == 'POST':
        form = AparelhoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aparelho cadastrado com sucesso.')
            return redirect('consumo:add_ambiente')
    else:
        form = AparelhoForm()
    context['form'] = form
    return render(request, template_name, context)

def details_app(request, slug):
    aparelho = get_object_or_404(Aparelho, slug=slug)
    template_name = 'details_aparelho.html'
    context = {
        'aparelho':aparelho
    }
    return render(request, template_name, context)

class AppReadView(BSModalReadView):
    model = Aparelho
    template_name = 'details_modal_app.html'

#Create de classe baseada em view by django-bootstrap-modal
class AppModalCreate(BSModalCreateView):
    template_name = 'add_modal_aparelho.html'
    form_class = AppForm
    success_message = 'Aparelho criado com sucesso.'
    success_url = reverse_lazy('consumo:list_ambiente')

def save_ambiente(request):
    template_name = 'save_ambiente.html'
    context = {}
    if request.method == 'POST':
        form = AmbienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ambiente cadastrado com sucesso.')
           
            return redirect('consumo:list_ambiente')
    else:
        form = AmbienteForm()
    context['form'] = form
    return render(request, template_name, context)

#Funçao que insere o aparelho no ambiente especifico
def insert_app_amb(request, slug):
    ambientes = get_object_or_404(Ambiente, slug=slug)

    if request.method == 'POST':
        form = InsertAppForm(request.POST, instance=ambientes)
        if form.is_valid():
            form.save()
            messages.success = (request, 'Aparelhos, inseridos no ambiente com sucesso!')
            return redirect('consumo:list_ambiente')
    else:
        form = InsertAppForm(instance=ambientes)
    template_name = 'save_ambiente.html'
    context = {
        'form':form,
        'ambientes':ambientes
    }
    return render(request, template_name, context)

#Funçoes de atualizações de aparelho e ambiente
def edit_aparelho(request, slug):
    aparelhos = get_object_or_404(Aparelho, slug=slug)

    if request.method == 'POST':
        form = AparelhoForm(request.POST, instance=aparelhos)
        if form.is_valid():
            form.save()
            messages.success = (request, 'Aparelho alterado com sucesso!')
            return redirect('consumo:list_aparelho')
    else:
        form = AparelhoForm(instance=aparelhos)
    template_name = 'save_aparelho.html'
    context = {
        'form':form,
    }
    return render(request, template_name, context)

def edit_modal_aparelho(request, slug):
    aparelhos = get_object_or_404(Aparelho, slug=slug)

    if request.method == 'POST':
        form = AparelhoForm(request.POST, instance=aparelhos)
        if form.is_valid():
            form.save()
            messages.success = (request, 'Aparelho alterado com sucesso!')
            return redirect('consumo:list_aparelho')
    else:
        form = AparelhoForm(instance=aparelhos)
    template_name = 'add_modal_app.html'
    context = {
        'form':form,
    }
    return render(request, template_name, context)

def edit_ambiente(request, slug):
    ambientes = get_object_or_404(Ambiente, slug=slug)

    if request.method == 'POST':
        form = AmbienteForm(request.POST, instance=ambientes)
        if form.is_valid():
            form.save()
            messages.success = (request, 'Ambiente alterado com sucesso!')
            ambientes = Ambiente.objects.get(slug=slug)
            success_url = reverse_lazy('consumo:ambientes_apps_list', kwargs={slug:'ambiente.slug'})
    else:
        form = AmbienteForm(instance=ambientes)
    template_name = 'save_ambiente.html'
    context = {
        'form':form,
    }
    return render(request, template_name, context)

#Funçoes de Delete de aparelho e ambiente
def delete_aparelho(request, slug):
    aparelho = get_object_or_404(Aparelho, slug=slug)
    aparelho.delete()
    messages.success(request, 'Aparelho apagado com sucesso!')
    return redirect('consumo:list_aparelho')

def delete_ambiente(request, slug):
    ambiente = get_object_or_404(Ambiente, slug=slug)
    ambiente.delete()
    messages.success(request, 'Ambiente apagado com sucesso!')
    return redirect('consumo:list_ambiente')

def delete_app_ambiente(request, pk, slug, ):   
    template_name = 'delete_app_ambiente.html'
    context ={}
    app = get_object_or_404(Aparelho, pk=pk)
    print(app)
    amb = get_object_or_404(Ambiente, slug=slug)
    print(amb)
    if request.method == 'POST':
        app.aparelhos_no_ambiente.remove(amb)
        messages.success(request, 'Aparelho apagado do ambiente com sucesso!')
        ambiente = Ambiente.objects.get(slug=slug)
        return redirect('consumo:ambientes_apps_list', slug=ambiente.slug)
    
    context = {
        app:'app',
        amb:'amb'
    }
    print(context)
    return render(request, template_name, context)
    
'''''' 
#Delete de classe baseada em view by django-bootstrap-modal
class Delete_App(BSModalDeleteView):
    slug_field = Ambiente.slug
    print(slug_field)
    model = Aparelho    
    template_name = 'delete_app_ambiente.html'
    success_message = 'Sucesso: Aparelho removido!'
    success_url = reverse_lazy('consumo:ambientes_apps_list', kwargs={slug_field})

#função que mostra uma lista de aparelhos ambientes
def list_aparelho(request):
    aparelho = Aparelho.objects.all()
    context = {
        'aparelhos':aparelho
    }
    template_name = 'dashboard_aparelho.html'
    return render(request, template_name, context)

def list_ambiente(request):
    ambientes = Ambiente.objects.all()
    context = {
        'ambientes':ambientes
    }
    template_name = 'details_ambiente.html'
    return render(request, template_name, context)

#Funçao que traz todos os aperelhos de um respectivo ambiente
def list_ambiente_aparelho(request, slug):
    aparelhos = Aparelho.objects.prefetch_related('aparelhos_no_ambiente'
    ).filter(aparelhos_no_ambiente__slug=slug)
    qnt = 0
    kwh = []
    time = 0
    hora = 0
    min = 0
    for aparelho in aparelhos:
        qnt += aparelho.quantidade
        if aparelho.status == 1:
            time = aparelho.tempo / 60
            kwh.append((aparelho.potencia * time) / 1000)
        else:
           kwh.append((aparelho.potencia * aparelho.tempo) / 1000)
    print(kwh)
    #print(pot)
    time = hora + min
    #print(time)
    #sub_total = (qnt * pot * time)/1000
    total = sum(kwh) * 30
    tarifa = total * 0.733363
    context = {
        'aparelhos':aparelhos,
        'ambientes':Ambiente.objects.get(slug=slug),
        'total':f'{total:.2f}'.replace('.', ','),
        'tarifa':f'{tarifa:.2f}'.replace('.', ',')
    }
    template_name = 'detalhes_aparelho.html'
    return render(request, template_name, context)