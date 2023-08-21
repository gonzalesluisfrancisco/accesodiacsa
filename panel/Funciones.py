from django.contrib.auth import  authenticate
import pytz
from datetime import datetime
import smtplib
from email.message import EmailMessage 
import random

def FormatoLoginValidos(Usuario, Contrasena, Captcha):
    Resultado = False
    Mensaje = ""
    if len(Usuario) < 6: Mensaje = "El usuario debe tener 6 caracteres como mínimo."
    elif len(Contrasena) < 8: Mensaje = "La contraseña debe tener 8 caracteres como mínimo."
    elif len(Captcha) < 10: Mensaje = "El captcha no ha sido resuelto."
    else: Resultado = True
    return Resultado, Mensaje

def DatosLoginValidos(request, Usuario, Contrasena):
    User = authenticate(request, username=Usuario, password=Contrasena)
    if User is None: return False, "El usuario o contraseña no es correcto"
    else: return True, "El usuario y contraseña son correctos"
    
def GenerarToken(Usuario, Contrasena, request):
    FechaHora_Timestamp = datetime.now(pytz.timezone('America/Lima')).timestamp()
    #Se debe generar un token
    #[a][n][o][x][p][y][q][b]
    #          a     b
    random.seed(FechaHora_Timestamp)
    a = b = random.randint(1,6)
    while a == b: b = random.randint(1,6) #Hasta aqui tengo a y b
    #
    FechaHora_Minutos = datetime.now(pytz.timezone('America/Lima')).strftime("%M")
    x = int(FechaHora_Minutos[0])
    y = int(FechaHora_Minutos[1])
    random.seed(a+b+x+y)
    Dummy = [random.randint(0,9), random.randint(0,9), random.randint(0,9), random.randint(0,9)]
    ArrayToken = [-1,-1,-1,-1,-1,-1,-1,-1]
    ArrayToken[0] = a
    ArrayToken[7] = b
    ArrayToken[a] = x
    ArrayToken[b] = y
    index = 0
    for i in range (1,7):
        if i == a or i == b: continue
        ArrayToken[i] = Dummy[index]
        index = index + 1
    Token = "".join(str(entero) for entero in ArrayToken)
    print(Token)
    User = authenticate(request, username = Usuario, password = Contrasena)
    EnviaCorreo(Usuario, User.email, Token)
    
    
    
def EnviaCorreo(Usuario, Destino, Token):
    email_subject = "Codigo de acceso - DIACSA" 
    sender_email_address = "pruebapythonenvioemail@gmail.com" 
    receiver_email_address = Destino
    email_smtp = "smtp.gmail.com" 
    email_password = "nxolslszfpecabmd" 
    message = EmailMessage() 
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 
    html_content = f"""\
    <html>
    <head></head>
    <body>
        <p>Hola, <span style="font-size: larger;">{Usuario}</span>!</p>
        <p>Este es tu token de verificación: <span style="font-size: larger;"><b>{Token}</b></span></p>
    </body>
    </html>
    """
    message.add_alternative(html_content, subtype='html')
    server = smtplib.SMTP(email_smtp, '587') 
    server.ehlo() 
    server.starttls() 
    server.login(sender_email_address, email_password) 
    server.send_message(message) 
    server.quit()
    
def VerificarToken(TokenIngresado):
    a = int(TokenIngresado[0])
    b = int(TokenIngresado[7])
    if a == 0 or a == 7 or b == 0 or b == 7 or b == a: return False
    x = int(TokenIngresado[a])
    y = int(TokenIngresado[b])
    MinutosAnteriores = x * 10 + y
    FechaHora_Minutos = datetime.now(pytz.timezone('America/Lima')).strftime("%M")
    MinutosActuales = int(FechaHora_Minutos)
    if MinutosActuales < MinutosAnteriores: MinutosActuales = MinutosActuales + 60
    if MinutosActuales - MinutosAnteriores > 2: return False
    random.seed(a+b+x+y)
    Dummy = [random.randint(0,9), random.randint(0,9), random.randint(0,9), random.randint(0,9)]
    ArrayToken = [-1,-1,-1,-1,-1,-1,-1,-1]
    ArrayToken[0] = a
    ArrayToken[7] = b
    ArrayToken[a] = x
    ArrayToken[b] = y
    index = 0
    for i in range (1,7):
        if i == a or i == b: continue
        ArrayToken[i] = Dummy[index]
        index = index + 1
    TokenCalculado = "".join(str(entero) for entero in ArrayToken)
    if TokenCalculado == TokenIngresado: return True
    else: return False