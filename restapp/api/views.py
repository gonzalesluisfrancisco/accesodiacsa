from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from restapp.models import PostCardIDEvent
from restapp.api.serializers import restappSerializer
#from rest_framework.decorators import action
#from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import viewsets
from panel.models import PersonalRegistrado
from panel.models import LiveData
from panel.models import Historial
from panel.models import NoRegistrados
from panel.models import deviceID

from django.http.response import HttpResponse

from datetime import datetime
#from django.utils import timezone
from zoneinfo import ZoneInfo
import pytz
from django.http import JsonResponse
import json
import re


##########################################

def cardIDValido(cardIDs):
    N = len(cardIDs)
    if N <1:
        print("cantidad de cardIDs no valido")
        return 0
    
    for cardID in cardIDs:
        cardID = cardID.upper()
        if(len(cardID)!=8):
            print("Longitud de cardID no valido")
            return 0
        for c in cardID:
            if not((c>='0' and c<='9') or (c>='A' and c<='F')):
                print("cardID no valido")
                return 0
    
    return N

def f_eventoValido(f_eventos):
    N = len(f_eventos)
    if N <1:
        print("cantidad de f_eventos no valido")
        return 0 

    for f_evento in f_eventos:
        if len(f_evento) != 10:
            print("Longitud de f_evento no valido")
            return 0                      
        try:
            datetime.strptime(f_evento, '%Y-%m-%d')
        except:
            print("Formato de f_evento no valido")
            return 0
    
    return N

def h_eventoValido(h_eventos):
    N = len(h_eventos)
    if N <1:
        print("cantidad de h_eventos no valido")
        return 0 

    for h_evento in h_eventos:
        if len(h_evento) != 8:
            print("Longitud de f_evento no valido")
            return 0                      
        try:
            datetime.strptime(h_evento, '%H:%M:%S')
        except:
            print("Formato de h_evento no valido")
            return 0
    
    return N

def eventoValido(eventos):
    N = len(eventos)
    if N <1:
        print("cantidad de eventos no valido")
        return 0 

    for evento in eventos:
        if evento != "Ingreso" and evento != "Salida":
            print("Evento no valido")
            return 0                      
    
    return N

def validar_hora(hora_str):
    """Valida el formato de la hora y lo ajusta si es necesario."""
    print("Validar hora")
    #print(hora_str)
    hora_patron = re.compile(r'^\d{1,2}:\d{1,2}(:\d{1,2})?$')
    if not hora_patron.match(hora_str):
        raise ValueError('La hora debe tener el formato "H:m:s" o "H:m".')
    partes = hora_str.split(':')
    #print(partes)
    if len(partes) == 2:
        hora_str += ':00'
    #print(hora_str)
    return hora_str

def validacionDataJson1(dataJson):
    try:
        dataJson = dict(dataJson)
    except:
        print("dataJson vacio o incorrecta")
        return [[],[],[],[],[]]
    
    deviceID=dataJson.pop('deviceID',None)
    if deviceID is None:
        print("No hay deviceID")
        return [[],[],[],[],[]]  
    if len(deviceID) !=1:
        print("No device ID valido")
        return [[],[],[],[],[]]
    
    cardID = dataJson.pop('cardID',None)
    if cardID is None:
        print("No hay cardID")
        return [[],[],[],[],[]]  
    N = cardIDValido(cardID)
    if N == 0:
        return [[],[],[],[],[]]

    f_evento = dataJson.pop('f_evento',None)
    if f_evento is None:
        print("No hay f_evento")
        return [[],[],[],[],[]]  
    if f_eventoValido(f_evento)!=N:
        return [[],[],[],[],[]]
    
    h_evento=dataJson.pop('h_evento',None)
    if h_evento is None:
        print("No hay h_evento")
        return [[],[],[],[],[]]  
    if h_eventoValido(h_evento)!=N:
        return [[],[],[],[],[]]
    
    evento=dataJson.pop('evento',None)
    if evento is None:
        print("No hay evento")
        return [[],[],[],[],[]]  
    if eventoValido(evento)!=N:
        return [[],[],[],[],[]]

    return [deviceID, cardID, f_evento, h_evento, evento]

def validacionDataJson(dataJson):
    try:
        dataJson = dict(dataJson)
    except:
        print("dataJson vacio o incorrecta")
        return []
    
    deviceID=dataJson.pop('deviceID',None)
    if deviceID is None:
        print("No hay deviceID")
        return []  
    if len(deviceID) !=1:
        print("No device ID valido")
        return []
    
    cardID = dataJson.pop('cardID',None)
    if cardID is None:
        print("No hay cardID")
        return []  
    N = cardIDValido(cardID)
    if N == 0:
        return []

    f_evento = dataJson.pop('f_evento',None)
    if f_evento is None:
        print("No hay f_evento")
        return []  
    if f_eventoValido(f_evento)!=N:
        return []
    
    h_evento=dataJson.pop('h_evento',None)
    if h_evento is None:
        print("No hay h_evento")
        return []  
    if h_eventoValido(h_evento)!=N:
        return []
    
    evento=dataJson.pop('evento',None)
    if evento is None:
        print("No hay evento")
        return []  
    if eventoValido(evento)!=N:
        return []

    datavalidada = []
    for i in range(N):
        datavalidada.append([deviceID[0],cardID[i], f_evento[i], h_evento[i], evento[i]])
    
    return datavalidada

    # Elimina la clave 'querySet' si existe
    if 'querySet' in dataJson:
        del dataJson['querySet']
    print("Segunda a json dumps conversion")
    dataJson = json.dumps(dataJson)
    print(dataJson)
    
    try:
        #print("1")
        dataJson = json.loads(dataJson)
    except:
        #print("2")
        return False
    print("Tercera a json dumps conversion")
    print(dataJson)

    
    #dataJson.pop('csrfmiddlewaretoken',None)
    #cardid = models.IntegerField(null=False)
    #f_evento = models.DateField(null=True)
    #h_evento = models.TimeField(null=True)
    #evento = models.CharField(max_length=50, null=True)
    
    #print(dataJson)


    
    campos_esperados = ['cardid', 'f_evento', 'h_evento', 'evento']
    #print(set(dataJson.keys()))
    #print(set(campos_esperados))
    if set(dataJson.keys()) != set(campos_esperados):
        #print("3")
        return False
    #print("3.1")
    for campo in campos_esperados:
        if campo not in dataJson:
            #print("4")
            #print(f"Falta el campo {campo} en el objeto JSON")
            return False
    #print("4.1")
    #Otra opcion es implementarlo
    #if not all(campo in data for campo in campos_esperados):
    #    False
    #print(dataJson['cardid'][0])
    if int(dataJson['cardid'][0])<0 or int(dataJson['cardid'][0])>5000000:
        #print("5")
        return False
    #print("5.1")
    if dataJson['evento'][0] not in ["Ingreso", "Salida"]:
        #print("6")
        return False  
    #print("6.1")
    #print(dataJson['f_evento'][0])
    try:
        datetime.strptime(dataJson['f_evento'][0], '%Y-%m-%d')
    except:
        #print("7")
        return False
    #print("7.1")
    try:
        hora_valida = validar_hora(dataJson['h_evento'][0])
    except ValueError as err:
        #print("8")
        #print("Error" + err)
        return False
    #print(dataJson['h_evento'])
    #print(dataJson['h_evento'][0])
    dataJson['h_evento'][0] = hora_valida
    #print("Se modifica hora")
    #print(dataJson['h_evento'])
    #print(dataJson['h_evento'][0])
    #print(dataJson)
    return True


def actualizarLiveDataNoRegistrado(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        print("Ubicacion LiveNoRegistrados")
        print(rubicacion)
        if(rubicacion is None):
            print("Ubicacion no encontrada en Live Data No Registrados")
            rubicacion = "No registrado"  
    except:
        print("Error en encontrar la ubicacion del deviceID en LiveData No Registrados.")
        rubicacion = "No registrado"   

    if(revento=="Ingreso"):
        print("Ingreso registrado en LiveData No Registrados")
        existenteLiveData = LiveData.objects.filter(cardidHex=rcardID).first()
        while existenteLiveData is not None: 
            existenteLiveData = LiveData.objects.filter(cardidHex=rcardID).first()
            if existenteLiveData is not None:
                existenteLiveData.delete()
        
        #usersLiveData = LiveData.objects.all()
        #cantidadactualRegistrada = usersLiveData.count()

        nuevoLiveData = LiveData()
        #nuevoLiveData.id = cantidadactualRegistrada+1
        nuevoLiveData.ubicacion = rubicacion
        nuevoLiveData.cardidHex = rcardID
        nuevoLiveData.nombre = "No registrado"
        nuevoLiveData.apellido = "No registrado"
        nuevoLiveData.empresa = "No registrado"
        nuevoLiveData.cargo = "No registrado"
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        print(fecha_datetime)
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
        nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
        print(nuevoLiveData)
        nuevoLiveData.save()
        print("Guardado como ingreso en LiveData exitoso.")
        return
    elif(revento=="Salida"):
        print("Salida en LiveData No Registrado")
        try:
            datosUserLiveData = LiveData.objects.get(cardidHex=rcardID)
            if(datosUserLiveData is not None):
                print("Intenta borrar en LiveData No Registrados")
                datosUserLiveData.delete()
                return
            else:
                print("No está en la tabla de LiveData No registrados")
                return
        except:
            print("Except luego de intentar borrar o encontrar. Puede ser porque no encuentra en LiveData.")
            return
    else:
        print("Evento desconocido en LiveData No Registrados")
        return   

def actualizarLiveDataRegistrados(reg):
    
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]
    
    try:
        datosUserLiveData = PersonalRegistrado.objects.get(cardidHex=rcardID)
        if(datosUserLiveData is None):
            print("Usuario no encontrado en Live Data Registrados")
            return 
    except:
        print("Error en encontrar el usuario en Live Data Registrados.")
        return

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if(rdeviceID is None):
            print("Ubicacion no encontrada")
            rubicacion = "No registrado"  
    except:
        print("Error en encontrar la ubicacion del deviceID.")
        rubicacion = "No registrado"   

    if(revento=="Ingreso"):
        print("Ingreso registrado en LiveData")
        existenteLiveData = LiveData.objects.filter(cardidHex=rcardID).first()
        while existenteLiveData is not None: 
            existenteLiveData = LiveData.objects.filter(cardidHex=rcardID).first()
            if existenteLiveData is not None:
                existenteLiveData.delete()
        
        #usersLiveData = LiveData.objects.all()
        #cantidadactualRegistrada = usersLiveData.count()

        nuevoLiveData = LiveData()
        #nuevoLiveData.id = cantidadactualRegistrada+1
        nuevoLiveData.ubicacion = rubicacion
        nuevoLiveData.cardidHex = datosUserLiveData.cardidHex
        nuevoLiveData.nombre = datosUserLiveData.nombre
        nuevoLiveData.apellido = datosUserLiveData.apellido
        nuevoLiveData.empresa = datosUserLiveData.empresa
        nuevoLiveData.cargo = datosUserLiveData.cargo
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
        nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
        nuevoLiveData.save()
        print("Guardado como ingreso en LiveData exitoso.")
        return
    elif(revento=="Salida"):
        print("Salida en LiveData")
        try:
            datosUserLiveData = LiveData.objects.get(cardidHex=rcardID)
            if(datosUserLiveData is not None):
                print("Intenta borrar")
                datosUserLiveData.delete()
                return
            else:
                print("No está en la tabla de LiveData")
                return
        except:
            print("Except luego de intentar borrar. Puede ser porque no encuentra en LiveData.")
            return
    else:
        print("Evento desconocido en LiveData")
        return   

def guardarHistorialRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if(rdeviceID is None):
            print("Ubicacion no encontrada en Historial Registrados")
            rubicacion = "No registrado"  
    except:
        print("Error en encontrar la ubicacion del deviceID en Historial Registrados.")
        rubicacion = "No registrado"  

    try:
        datosUserHistorial = PersonalRegistrado.objects.get(cardidHex=rcardID)
        if(datosUserHistorial is None):
            print("Usuario no encontrado en historial Registrados")
            return 
        
        usersHistorial = Historial.objects.all()
        cantidadactualRegistrada = usersHistorial.count()
        nuevoHistorial = Historial()
        nuevoHistorial.id = cantidadactualRegistrada+1
        nuevoHistorial.ubicacion = rubicacion
        nuevoHistorial.cardidHex = datosUserHistorial.cardidHex
        nuevoHistorial.nombre = datosUserHistorial.nombre
        nuevoHistorial.apellido = datosUserHistorial.apellido
        nuevoHistorial.empresa = datosUserHistorial.empresa
        nuevoHistorial.cargo = datosUserHistorial.cargo
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        print(zona_horaria)
        #fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc) 
        #fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoHistorial.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoHistorial.evento = revento
        nuevoHistorial.save()
        return
        
    except:
        print("Error al guardar en Historial Registrados.")
        return

def guardarHistorialNoRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if(rdeviceID is None):
            print("Ubicacion no encontrada en Historial No Registrados")
            rubicacion = "No registrado"  
    except:
        print("Error en encontrar la ubicacion del deviceID en Historial No registrados.")
        rubicacion = "No registrado"  

    try:
        
        usersHistorial = Historial.objects.all()
        cantidadactualRegistrada = usersHistorial.count()
        nuevoHistorial = Historial()
        nuevoHistorial.id = cantidadactualRegistrada+1
        nuevoHistorial.ubicacion = rubicacion
        nuevoHistorial.cardidHex = rcardID
        nuevoHistorial.nombre = "No Registrado"
        nuevoHistorial.apellido = "No Registrado"
        nuevoHistorial.empresa = "No Registrado"
        nuevoHistorial.cargo = "No Registrado"
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoHistorial.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoHistorial.evento = revento
        nuevoHistorial.save()
        return
        
    except:
        print("Error al guardar en Historial No Registrados.")
        return

def guardarNoRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]
    print("Inicio evento en No Registrados")
    print(reg)
    try:
        print("rdeviceID")
        print(rdeviceID)
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        print("Ubicacion")
        print(rubicacion)
        if(rdeviceID is None):
            print("Ubicacion no encontrada en No Registrados")
            rubicacion = "Ubicacion No registrada"  
    except:
        print("Error en encontrar la ubicacion del deviceID en No Registrados.")
        rubicacion = "Ubicacion No registrada"   
    
    #usersNoRegistrados = NoRegistrados.objects.all()
    #cantidadactualRegistrada = usersNoRegistrados.count()
    #print("Cantidad actual")
    #print(cantidadactualRegistrada)
    nuevoNoRegistrados = NoRegistrados()
    #nuevoNoRegistrados.id = cantidadactualRegistrada+1
    nuevoNoRegistrados.ubicacion = rubicacion
    nuevoNoRegistrados.cardidHex = rcardID
    f_evento = rfecha_evento
    h_evento = rhora_evento
    fecha_datetime = datetime.strptime(f_evento+' '+h_evento,'%Y-%m-%d %H:%M:%S')
    zona_horaria = pytz.timezone('America/Lima')
    fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
    nuevoNoRegistrados.f_evento = fecha_y_hora_con_zona_horaria.date()
    nuevoNoRegistrados.h_evento = fecha_y_hora_con_zona_horaria.time()
    nuevoNoRegistrados.evento = revento
    nuevoNoRegistrados.save()
    print("Evento guardado en No Registrados exitoso.")
    return
    

class restappViewSet(ModelViewSet):
    serializer_class = restappSerializer
    queryset = PostCardIDEvent.objects.all()

    def create(self, request):
        data = request.data

        #Validacion de datos
        try:
            #print('DATA QUE LLEGA A LA VISTA CREATE POR DEFECTO')
            #print(data)
            registros = validacionDataJson(data)
            N = len(registros)
            if N == 0:
                return JsonResponse({'error': 'Verificar campos'}, status=400)
        except:
            return JsonResponse({'error': 'Error inesperado en campos'}, status=400)
        
        for i in range(N):
            reg = registros[i]
            rcardID = reg[1]
            print("-------------")
            try:
                user = PersonalRegistrado.objects.get(cardidHex=rcardID)    
                if(user is None):
                    print("Usuario no encontrado")
            except:
                print("Usuario no encontrado except")
                print("1")
                actualizarLiveDataNoRegistrado(reg)
                print("2")
                guardarHistorialNoRegistrados(reg)
                print("3")
                guardarNoRegistrados(reg)
                continue


            #####################################
            try:
                print("Usuario encontrado. Se registrará en 'Live Data' e 'Historial'")
                actualizarLiveDataRegistrados(reg)
                guardarHistorialRegistrados(reg)
                
            except:
                print("Error en actualizar en base de datos. Se registrará en 'No Registrados' e 'Historial'.")
                continue                
        return JsonResponse({'envio': 'OK'}, status=200) #super().create(request)
