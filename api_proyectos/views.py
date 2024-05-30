from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from .models import Proyectos, Tarea

# Create your views here.


def index(request):

    if request.method == 'POST':
        name = request.POST.get('nombre_proyecto')
        description = request.POST.get('descripcion_proyecto')

        if not (name and description):
            error_message = 'El proyecto debe tener un nombre'
            return render(request, 'index.html', {
                'error_message': error_message,
                'proyectos': proyectos
            })

        Proyectos.objects.create(nombre=name, descripcion=description)

        proyectos = list(Proyectos.objects.all())

        return render(request, 'index.html', {
            'proyectos': proyectos
        })

    else:
        proyectos = list(Proyectos.objects.all())

        return render(request, 'index.html', {
            'proyectos': proyectos
        })


def proyecto(request, nombre):
    error_message = request.session.pop('error_message', None)
    error_fecha = request.session.pop('error_fecha', None)

    proyecto = Proyectos.objects.get(nombre=nombre)
    tareas = list(Tarea.objects.filter(proyecto=proyecto.id))

    date_hoy = datetime.now().date()

    for tarea in tareas:
        if tarea.fecha_fin < date_hoy:
            tarea.estado = True
            tarea.save()

    for tarea in tareas:
        if tarea.estado == False:
            proyecto.estado = False
            proyecto.save()
            break
        else:
            proyecto.estado = True
            proyecto.save()

    return render(request, 'proyectos/proyecto.html', {
        'proyecto': proyecto,
        'tareas': tareas,
        'error_message': error_message,
        'error_fecha': error_fecha,
    })


def add_tarea(request):
    if request.method == 'POST':
        id_proyecto = request.POST.get('id_proyecto')
        proyecto = get_object_or_404(Proyectos, id=id_proyecto)

        nombre = request.POST.get('nombre_tarea')
        fecha_ini = request.POST.get('date_ini')
        fecha_fin = request.POST.get('date_fin')

        if not (nombre and fecha_ini and fecha_fin):
            error_message = 'Los campos no pueden estar vacios'
            request.session['error_message'] = error_message
            return redirect(reverse('proyecto', args=[proyecto.nombre]))

        if fecha_fin < fecha_ini:
            error_fecha = 'La fecha de finalización no puede ser menor que la fecha de inicio'
            request.session['error_fecha'] = error_fecha
            return redirect(reverse('proyecto', args=[proyecto.nombre]))

        date_hoy = datetime.now().date()
        date_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        if date_fin < date_hoy:
            estado = True
            Tarea.objects.create(nombre=nombre, fecha_ini=fecha_ini,
                                 fecha_fin=fecha_fin, estado=estado, proyecto=proyecto)
        else:
            Tarea.objects.create(nombre=nombre, fecha_ini=fecha_ini,
                                 fecha_fin=fecha_fin, proyecto=proyecto)

        # La función (redirect(reverse)) está reedireccionando a una vista que contiene el nombre de la url y un argumento como requerimiento para poder acceder a la vista
        return redirect(reverse('proyecto', args=[proyecto.nombre]))


def edit(request):
    if request.method == 'POST':
        id_proyecto = request.POST.get('id_proyecto')
        proyecto = get_object_or_404(Proyectos, id=id_proyecto)

        name = request.POST.get('nombre_proyecto')
        description = request.POST.get('descripcion_proyecto')

        if not name:
            error_message = 'El proyecto debe tener un nombre'
            request.session['error_message'] = error_message
            return redirect(reverse('proyecto', args=[proyecto.nombre]))

        proyecto.nombre = name
        proyecto.descripcion = description
        proyecto.save()

        return redirect(reverse('proyecto', args=[proyecto.nombre]))


def tarea(request, id):

    error_message = request.session.pop('error_message', None)
    error_fecha = request.session.pop('error_fecha', None)
    tarea = get_object_or_404(Tarea, id=id)
    proyecto = tarea.proyecto

    return render(request, 'tareas/tarea.html', {
        'tarea': tarea,
        'error_message': error_message,
        'error_fecha': error_fecha,
        'proyecto': proyecto,
    })


def edit_task(request):
    if request.method == 'POST':
        id_tarea = request.POST.get('id_tarea')
        tarea = get_object_or_404(Tarea, id=id_tarea)

        nombre = request.POST.get('nombre_tarea')
        fecha_ini = request.POST.get('date_ini')
        fecha_fin = request.POST.get('date_fin')

        if not (nombre and fecha_ini and fecha_fin):
            error_message = 'Los campos no pueden estar vacios'
            request.session['error_message'] = error_message
            return redirect(reverse('tarea', args=[tarea.id]))
        
        if fecha_fin < fecha_ini:
            error_fecha = 'La fecha de finalización no puede ser menor que la fecha de inicio'
            request.session['error_fecha'] = error_fecha
            return redirect(reverse('tarea', args=[tarea.id]))

        date_hoy = datetime.now().date()
        date_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        tarea.nombre = nombre
        tarea.fecha_ini = fecha_ini
        tarea.fecha_fin = fecha_fin
        tarea.save()

        if date_fin < date_hoy:
            tarea.estado = True
            tarea.save()
        else:
            tarea.estado = False
            tarea.save()

        return redirect(reverse('tarea', args=[tarea.id]))


def eliminar_tarea(request, nombre, id):
    tarea = get_object_or_404(Tarea, id=id)
    proyecto = get_object_or_404(Proyectos, nombre=nombre)

    tarea.delete()

    return redirect(reverse('proyecto', args=[proyecto.nombre]))


def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyectos, id=id)
    proyecto.delete()
    return redirect('/')


def actualizarEstado(request, id):
    proyecto = get_object_or_404(Proyectos, id=id)
    proyecto.estado = True
    proyecto.save()

    date_hoy = datetime.now().date()
    tareas = Tarea.objects.filter(proyecto=proyecto.id)

    for tarea in tareas:
        if tarea.fecha_fin >= date_hoy:
            tarea.fecha_fin = date_hoy
            tarea.estado = True
            tarea.save()

    return JsonResponse({
        'message': 'Estado acutualizado correctamente'
    })
