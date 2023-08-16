from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from . import models

#from datetime import datetime
from django.utils import timezone
from django.utils.timezone import activate
import pytz

from django.db.models import Q

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def index_noautenticado(request):
    
    return render(request, "index.html")

def autenticacion(request):
    if request.method == 'GET':
        return render(request, "login.html",{
            'error': 'Hola Andre.'
        })
    
    user = authenticate(
        request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'login.html', {
            'error': 'Username or password incorrect'
        })
    else:
        login(request, user)
        return redirect('livedata')    
    
@login_required(login_url = 'autenticacion')
def signout(request):
    logout(request)
    return redirect("autenticacion")

@login_required(login_url = 'autenticacion')
def index(request):
    print("Ingreso a intentar leer el livedata")
    users = models.LiveData.objects.all()
    data = {'total': users.count()}
    return render(request, "index.html", data)

@login_required(login_url = 'autenticacion')
def listar(request):
    users = models.PersonalRegistrado.objects.all()
    datos = { 'personalregistrado' : users}
    return render(request, "crud_aesadiacsa/listar.html", datos)

@login_required(login_url = 'autenticacion')
def agregar(request):
    if request.method == 'POST':
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('empresa'))
        print(request.POST.get('cargo'))
        print(request.POST.get('telefono'))
        print(request.POST.get('correo'))
        print(request.POST.get('f_nac'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('telefono') and request.POST.get('correo') and request.POST.get('f_nac'):
            users = models.PersonalRegistrado.objects.all()
            cantidadactualRegistrada = users.count()
            user = models.PersonalRegistrado()
            user.id = cantidadactualRegistrada+1
            user.cardidHex = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.empresa = request.POST.get('empresa')
            user.cargo = request.POST.get('cargo')
            user.correo = request.POST.get('correo')
            user.telefono = request.POST.get('telefono')
            user.f_nac = request.POST.get('f_nac')
            user.f_registro = timezone.now()
            user.save()
            return redirect('listar')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "crud_aesadiacsa/agregar.html", datos)

    else:
        return render(request, "crud_aesadiacsa/agregar.html")

@login_required(login_url = 'autenticacion')
def actualizar(request, codigo):
    if request.method == 'POST':
        #print(request.POST.get('id'))
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('empresa'))
        print(request.POST.get('cargo'))
        print(request.POST.get('telefono'))
        print(request.POST.get('correo'))
        print(request.POST.get('f_nac'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('id') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('telefono') and request.POST.get('correo') and request.POST.get('f_nac'):
            user = models.PersonalRegistrado()
            #user.id = request.POST.get('id')
            user.cardidHex = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.empresa = request.POST.get('empresa')
            user.cargo = request.POST.get('cargo')
            user.correo = request.POST.get('correo')
            user.telefono = request.POST.get('telefono')
            user.f_nac = request.POST.get('f_nac')
            user.f_registro = timezone.now()
            user.save()
            return redirect('listar')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "crud_aesadiacsa/actualizar.html", datos)    
    else:
        datosuser = models.PersonalRegistrado.objects.get(cardidHex=codigo)
        print("Obtuvo datos de usuario")
        print(datosuser)
        datos = { 'personalregistrado' : datosuser} 

        return render(request, "crud_aesadiacsa/actualizar.html", datos)

@login_required(login_url = 'autenticacion')
def eliminar(request, codigo):
    tupla = models.PersonalRegistrado.objects.get(cardidHex=codigo)
    tupla.delete()
    return redirect('listar')

@login_required(login_url = 'autenticacion')
def livedata(request):
    users = models.LiveData.objects.all()
    #activate(pytz.timezone('America/Lima'))
    #print(timezone.now())
    datos = { 'livedata' : users,
             'fecha_y_hora': timezone.now(),
             'total': users.count()}
    return render(request, "livedata/livedata.html", datos)

@login_required(login_url = 'autenticacion')
def livedata_llenar(request):
    users = models.LiveData.objects.all()
    #users.
    #datosuser = models.PersonalRegistrado.objects.get(id=codigo)
    return redirect('livedata')

@login_required(login_url = 'autenticacion')
def livedata_agregar(request):
    if request.method == 'POST':
        print(request.POST.get('cardid'))
        print(request.POST.get('nombre'))
        print(request.POST.get('apellido'))
        print(request.POST.get('cargo'))
        print(request.POST.get('f_ingreso'))
        print(request.POST.get('h_ingreso'))
        #agregar datos
        if request.POST.get('cardid') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('cargo') and request.POST.get('f_ingreso') and request.POST.get('h_ingreso'):
            users = models.LiveData.objects.all()
            cantidadactualRegistrada = users.count()
            user = models.LiveData()
            user.id = cantidadactualRegistrada+1
            user.cardid = request.POST.get('cardid')
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.cargo = request.POST.get('cargo')
            user.f_ingreso = request.POST.get('f_ingreso')
            user.h_ingreso = request.POST.get('h_ingreso')
            user.save()
            return redirect('livedata')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "livedata/livedata_agregar.html", datos)

    else:
        return render(request, "livedata/livedata_agregar.html")

@login_required(login_url = 'autenticacion')
def livedata_eliminar(request):
    if request.method == 'POST':
        print(request.POST.get('cardidHex'))
        #agregar datos
        if request.POST.get('cardidHex'):
            cardidHex_a_borrar = request.POST.get('cardidHex')
            tupla = models.LiveData.objects.get(cardidHex=cardidHex_a_borrar)
            tupla.delete()
            return redirect('livedata')
        datos = { 'r2' : "Debe ingresar todos los campos correctamente"}
        return render(request, "livedata/livedata_eliminar.html", datos) 
    else:    
        users = models.LiveData.objects.all()
        datos = { 'livedata' : users} 
        return render(request, "livedata/livedata_eliminar.html", datos)

from django.core import serializers
from django.http import JsonResponse
@login_required(login_url = 'autenticacion')
def marcacion(request): 
    if request.method == "POST":
        print("Search")
        min = request.POST.get("min")
        max = request.POST.get("max")
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search_value = request.POST.get('search[value]', '')
        if search_value != '':
            queryset = models.Historial.objects.filter(
            Q(id__icontains=search_value) |
            Q(ubicacion__icontains=search_value) |
            Q(cardidHex__icontains=search_value) |
            Q(nombre__icontains=search_value) |
            Q(apellido__icontains=search_value) |
            Q(empresa__icontains=search_value) |
            Q(cargo__icontains=search_value) |
            Q(f_evento__icontains=search_value) |
            Q(h_evento__icontains=search_value) |
            Q(evento__icontains=search_value)
            ).order_by("-id")
        else:
            queryset = models.Historial.objects.order_by('-id')
        if min != "" and max != "":
            queryset = models.Historial.objects.filter(f_evento__range=(min, max)).order_by('-id')
        total_records = queryset.count()
        queryset = queryset[start:start+length]
        data = []
        for obj in queryset:
            item = {
                'id': obj.id,
                'ubicacion': obj.ubicacion,
                'cardidHex': obj.cardidHex,
                'nombre': obj.nombre,
                'apellido': obj.apellido,
                'empresa': obj.empresa,
                'cargo': obj.cargo,
                'f_evento': obj.f_evento,
                'h_evento': obj.h_evento,
                'evento': obj.evento,
            }
            data.append(item)
        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data
        }
        # print(response)
        return JsonResponse(response)
    print("Marcacion")
    # users = models.Historial.objects.all().order_by('-id')
    # datos = { 'marcacion' : users}
    # print(users[0].id, users[0].f_evento, type(users))
    return render(request, "marcacion/marcacion.html")

@login_required(login_url = 'autenticacion')
def noregistrados(request):
    users = models.NoRegistrados.objects.all()
    datos = { 'noregistrados' : users}
    return render(request, "noregistrados/noregistrados.html", datos)
