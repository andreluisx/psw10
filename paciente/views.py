from django.shortcuts import render, get_object_or_404, redirect
from medico.models import DatasAbertas, DadosMedico, Especialidades
from datetime import datetime
from .models import Consulta, Documento
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def home(request):
    medicos = DadosMedico.objects.filter(status='aprovado')
    especialidades = Especialidades.objects.all()
    
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades})
    
def escolher_horario(request, id_dados_medicos):
    medico = get_object_or_404(DadosMedico, id=id_dados_medicos)
    datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
 
    context = {
               'medico': medico, 
               'datas_abertas': datas_abertas, 
               }
    
    return render(request, 'escolher_horario.html', context)

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente = request.user,
            data_aberta=data_aberta,
        )
        horario_agendado.save()
        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, "Horario marcado com sucesso!")
        return redirect('/pacientes/minhas_consultas/')
    

def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas})

def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        consulta = Consulta.objects.get(id=id_consulta)
        documentos = Documento.objects.filter(consulta=consulta)

        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'documentos': documentos})