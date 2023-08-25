from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes

from . import models

#from datetime import datetime
from django.utils import timezone
from django.utils.timezone import activate
import pytz

from django.db.models import Q

from . import Funciones as Fun
from django.core.exceptions import ObjectDoesNotExist

import re
import random
import string
from datetime import datetime
import traceback
import openpyxl


# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def index_noautenticado(request):
    
    return render(request, "index.html")

def autenticacion(request):
    if request.method == "POST":
        
        if request.POST.get("Comando") == "VerificarLogin":
            Usuario = request.POST.get("Usuario")
            Contrasena = request.POST.get("Contrasena")
            Captcha = request.POST.get("Captcha")
            FormatoValido, Mensaje = Fun.FormatoLoginValidos(Usuario, Contrasena, Captcha)
            if not FormatoValido:
                return JsonResponse({"Estado": "Invalido", 'Mensaje': Mensaje})
            DatosValidos, Mensaje = Fun.DatosLoginValidos(request, Usuario, Contrasena)
            if DatosValidos:
                Correo = Fun.EnviarToken(Usuario, Contrasena, request)
                return JsonResponse({"Estado": "Valido", 'Mensaje': Mensaje, "Correo": Correo})
            return JsonResponse({"Estado": "Invalido", 'Mensaje': Mensaje})
        
        elif request.POST.get("Comando") == "VerificarToken":
            Usuario = request.POST.get("Usuario")
            Contrasena = request.POST.get("Contrasena")
            Token = request.POST.get("Token")
            if len(Token) != 8:
                return JsonResponse({"Estado": "Invalido", "Mensaje": "El Token debe ser de 8 digitos"})
            if not Fun.VerificarToken(Token):
                return JsonResponse({"Estado": "Invalido", 'Mensaje': "El token ingresado no es correcto"})
            DatosValidos, Mensaje = Fun.DatosLoginValidos(request, Usuario, Contrasena)
            if not DatosValidos:
                return JsonResponse({"Estado": "Invalido", 'Mensaje': "No deberias poder ver esto"})
            login(request, authenticate(request, username = Usuario, password = Contrasena))
            return JsonResponse({"Estado": "Valido", "Mensaje": "El token ha sido validado correctamente"})
        
        elif request.POST.get("Comando") == "RecuperarCuenta":
            Correo = request.POST.get("Correo")
            if len(Correo) == 0: return JsonResponse({"Estado": "Invalido", "Mensaje": "Debe ingresar su correo electronico"})
            try: Usuario = User.objects.get(email = Correo)
            except ObjectDoesNotExist: return JsonResponse({"Estado": "Invalido","Mensaje": "El correo ingresado no se encuentra registrado"})
            token = default_token_generator.make_token(Usuario)
            uid = urlsafe_base64_encode(force_bytes(Usuario.pk))
            current_site = get_current_site(request)
            Asunto = 'Recuperar contraseña - DIACSA'
            reset_url = f"https://{current_site}/reset-password/{uid}/{token}/"
            MensajeHTML = f"""\
            <html>
            <head></head>
            <body>
                <p>Hola, <span style="font-size: larger;">{Usuario.first_name}</span>!</p>
                <p>Entra a este enlace para recuperar tu contraseña: <br><span style="font-size: larger;"><b>{reset_url}</b></span></p>
            </body>
            </html>
            """
            Fun.EnviaCorreo(Usuario.email, Asunto, MensajeHTML)
            return JsonResponse({"Estado": "Valido", "Mensaje": "El enlace de recuperacion ha sido enviado a su correo"})
                
        else:
            return JsonResponse({"Estado": "Invalido", 'Mensaje': "El comando es desconocido"})
    
    signout(request)
    return render(request, "login.html")

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        try:
            UID = force_str(urlsafe_base64_decode(uidb64))
            Usuario = User.objects.get(pk=UID)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist): Usuario = None
        if Usuario is None or not default_token_generator.check_token(Usuario, token):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El enlace de recuperacion no es valido"})
        NuevaContrasena = request.POST.get('Contrasena1')
        ConfirmacionContrasena = request.POST.get('Contrasena2')
        if NuevaContrasena != ConfirmacionContrasena:
            return JsonResponse({"Estado": "Invalido", "Mensaje": "Las contraseñas ingresadas no coinciden"})
        if not Fun.ContrasenaEsFuerte(NuevaContrasena):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "La nueva contraseña debe tener:\nUna mayuscula.\nUna minuscula.\nSin numeros consecutivos.\nMinimo 8 caracteres"})
        Usuario.set_password(NuevaContrasena)
        Usuario.save()
        return JsonResponse({"Estado": "Valido", "Mensaje": "La contraseña se ha cambiado correctamente"})
    else:
        return render(request, 'reset_password.html')

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
    if request.method == "POST" and request.user.is_superuser:
        Comando = request.POST.get("Comando")
        ExcelFile = request.FILES.get("excelFile")
        if ExcelFile:
            try:
                Excel = openpyxl.load_workbook(ExcelFile)
                Hoja = Excel.active
                
                return JsonResponse({'Mensaje': 'Planilla actualizada correctamente', 'Estado': "Valido"})
            except Exception as e:
                return JsonResponse({'Estado': 'Invalido', 'Mensaje': str(e) + "\n" + traceback.format_exc()})
        return JsonResponse({"Estado":"Invalido","Mensaje":"El archivo no se ha podido leer"})
    users = models.PersonalRegistrado.objects.all()
    datos = { 'personalregistrado' : users}
    if request.user.is_staff:
        return render(request, "crud_aesadiacsa/listar.html", datos)
    return render(request, "crud_aesadiacsa/listar_basic.html", datos)    
    

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
    if request.method == "POST" and request.POST.get("Comando") == "TablaLiveData":
        print("Tabla LiveData")
        print("Search")
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search_value = request.POST.get('search[value]', '')
        queryset = models.LiveData.objects.order_by("-f_ingreso", "-h_ingreso")   
        if search_value != '':
            queryset = queryset.filter(
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
            ).order_by("-f_ingreso", "-h_ingreso")    
        total_records = queryset.count()
        queryset = queryset[start:start+length]
        data = []
        for i, obj in enumerate(queryset, start=0):
            item = {
                'id':str(total_records - start - i),
                'ubicacion': obj.ubicacion,
                'cardidHex': obj.cardidHex,
                'nombre': obj.nombre,
                'apellido': obj.apellido,
                'empresa': obj.empresa,
                'cargo': obj.cargo,
                'f_evento': obj.f_ingreso,
                'h_evento': obj.h_ingreso,
            }
            data.append(item)
        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data,
        }
        # print(response)
        return JsonResponse(response)
    elif request.method == "POST" and request.POST.get("Comando") == "ObtenerHoraTotal":
        print("ObtenerHoraTotal")
        lima_timezone = pytz.timezone('America/Lima')
        lima_time = timezone.now().astimezone(lima_timezone).strftime('%Y-%m-%d %H:%M:%S')
        total = models.LiveData.objects.order_by("-f_ingreso", "-h_ingreso").count()
        return JsonResponse({"Estado": "Valido", "Total": total, "Hora": lima_time})
    #users = models.LiveData.objects.all()
    #activate(pytz.timezone('America/Lima'))
    #print(timezone.now())
    #datos = { 'livedata' : users,             'fecha_y_hora': timezone.now(),             'total': users.count()}
    return render(request, "livedata/livedata.html")

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
    if request.method == "POST" and request.POST.get("Comando")=="TablaMarcacion":
        print("Search")
        min = request.POST.get("min")
        max = request.POST.get("max")
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search_value = request.POST.get('search[value]', '')
        queryset = models.Historial.objects.order_by('-id')
        if min != "" and max != "":
            queryset = queryset.filter(f_evento__range=(min, max)).order_by('-id')
        if search_value != '':
            queryset = queryset.filter(
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
    elif request.method == "GET" and request.GET.get("Comando") == "DescargarExcel":
        min = request.GET.get('FechaInicial')
        max = request.GET.get('FechaFinal')
        search_value = request.GET.get('Search', '')
        print(min, max)
        queryset = models.Historial.objects.order_by('-id')
        if min != "" and max != "":
            queryset = queryset.filter(f_evento__range=(min, max)).order_by('-id')
        if search_value != '':
            queryset = queryset.filter(
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
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['#', 'Ubicacion', 'Card ID', 'Nombre', 'Apellido', 'Cargo', 'F. Evento', 'H. Evento', 'Evento'])
        for item in queryset:
            ws.append([item.id, item.ubicacion, item.cardidHex, item.nombre, item.apellido, item.cargo, item.f_evento, item.h_evento, item.evento])
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Historial_ingresos_salidas.xlsx"'
        wb.save(response)
        return response
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

@login_required(login_url = 'autenticacion')
def registrarusuario(request):    
    if request.method == "POST":
        if request.POST.get("Comando") != "RegistrarUsuario":
            return JsonResponse({"Estado": "Invalido", "Mensaje": "¿Que haces?"})
        Nombre = request.POST.get("Nombre").strip().upper()
        PrimerApellido = request.POST.get("PrimerApellido").strip().upper()
        SegundoApellido = request.POST.get("SegundoApellido").strip().upper()
        DNI = request.POST.get("DNI").strip()
        Correo = request.POST.get("Correo").strip()
        Telefono = request.POST.get("Telefono").strip()
        is_staff = False
        if request.POST.get("Rol") == "Observador y registro de planilla": is_staff = True
        if not(len(Nombre) and len(PrimerApellido) and len(SegundoApellido) and len(DNI) and len(Correo) and len(Telefono)):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "Debe llenar todos los campos antes de continuar"})
        if not re.match(r'^[A-Za-z\s]+$', Nombre):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El nombre debe contener solo letras"})   
        if not re.match(r'^[A-Za-z]+$', PrimerApellido):
                return JsonResponse({"Estado": "Invalido", "Mensaje": "El apellido debe contener solo letras"}) 
        if not re.match(r'^[A-Za-z\s]+$', SegundoApellido):
                return JsonResponse({"Estado": "Invalido", "Mensaje": "El apellido debe contener solo letras"})  
        if len(DNI) != 8:
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El DNI debe tener 8 caracteres"})
        if not re.match(r'^\d+$', DNI):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "Debe ingresar un dni valido"})
        if models.UserInfo.objects.filter(DNI = DNI).exists():
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El DNI ya se encuentra registrado"})
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', Correo):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "Debe ingresar un correo valido"})
        if User.objects.filter(email = Correo).exists():
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El correo ya se encuentra registrado"})
        if len(Telefono) != 9:
            return JsonResponse({"Estado": "Invalido", "Mensaje": "El telefono debe tener 9 caracteres"})
        if not re.match(r'^\d+$', Telefono):
            return JsonResponse({"Estado": "Invalido", "Mensaje": "Debe ingresar un telefono valido"})
        try:
            Username = Nombre[0].lower() + PrimerApellido.lower() + DNI[4:8]
            if User.objects.filter(username = Username).exists():
                Username = Nombre[0].lower() + PrimerApellido.lower() + DNI[0:4]
            random.seed(int(datetime.now().timestamp()))
            Password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            NuevoUsuario = User(username = Username, email = Correo, first_name = Nombre, last_name = PrimerApellido, is_staff=is_staff)
            NuevoUsuario.set_password(Password)
            MensajeHTML = f"""\
            <html>
            <head></head>
            <body>
                <p>Hola, <span style="font-size: larger;">{NuevoUsuario.first_name}</span>!</p>
                <p>Se ha registrado su cuenta, sus datos de acceso son:</p>
                <p><br><span style="font-size: larger;"><b>Usuario: {NuevoUsuario.username}</b></span><br>
                <p><br><span style="font-size: larger;"><b>Contraseña: {Password}</b></span></p>
            </body>
            </html>
            """
            Fun.EnviaCorreo(NuevoUsuario.email, "Cuenta registrada - Control de acceso", MensajeHTML)
            NuevoUsuario.save()
            NuevoUsuarioInfo = models.UserInfo(User = NuevoUsuario, DNI = DNI, Telefono = Telefono, SegundoApellido = SegundoApellido)
            NuevoUsuarioInfo.save()
            print(Username, Password)
            return JsonResponse({"Estado": "Valido", "Mensaje": "Registrado correctamente, se ha enviado las credenciales al correo electronico"})
        except Exception as e:
            return JsonResponse({"Estado": "Invalido", "Mensaje": f"{str(e)}"})
        
        
    else:
        if request.user.is_superuser:
            return render(request, "registrarusuario/plantillaregistro.html")
        return render(request, "registrarusuario/plantilladenegado.html")

def eliminarusuario(request):
    if request.method == "POST":
        if request.POST.get("Comando") == "ConsultarDatos":
            Usuario = request.POST.get("Usuario")
            if not User.objects.filter(username = Usuario).exists():
                return JsonResponse({"Estado": "Invalido"})
            user = User.objects.get(username = Usuario)
            user2 = models.UserInfo.objects.get(User = user)
            Nombre = user.first_name
            PrimerApellido = user.last_name
            SegundoApellido = user2.SegundoApellido
            DNI = user2.DNI
            Correo = user.email
            Telefono = user2.Telefono
            Rol = "Solo observador"
            if user.is_staff: Rol = "Observador y registro de planilla"
            Data = {
                "Estado": "Valido",
                "Nombre": Nombre,
                "PrimerApellido": PrimerApellido,
                "SegundoApellido": SegundoApellido,
                "DNI": DNI,
                "Correo": Correo,
                "Telefono": Telefono,
                "Rol": Rol,
            }
            return JsonResponse(Data)
        elif request.POST.get("Comando") == "EliminarUsuario":
            try:
                Usuario = request.POST.get("Usuario")
                user = User.objects.get(username = Usuario)
                user.delete()
                return JsonResponse({"Estado": "Valido", "Mensaje": "El usuario se elimino correctamente"})
            except Exception as e:
                return JsonResponse({"Estado": "Invalido", "Mensaje": f"{str(e)}"})
                
    if request.user.is_superuser:
        Usuarios = User.objects.exclude(username = request.user.username)
        return render(request, "eliminarusuario/plantillaeliminar.html", {"Usuarios": Usuarios})
    return render(request, "eliminarusuario/plantilladenegado.html")
