from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PersonalRegistrado(models.Model):
    id = models.BigAutoField(primary_key=True)
    cardidHex = models.CharField(max_length=8, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    empresa = models.CharField(max_length=50, null=True)
    cargo = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length=50, null=False)
    telefono = models.IntegerField(null=True)
    f_nac = models.DateField(null=True)
    f_registro = models.DateTimeField(auto_now_add=True, null=False)
    servicio = models.CharField(max_length=50, null=False, default="No aplica")
    area = models.CharField(max_length=50, null=False, default="No aplica")

    def __str__(self):
        return str(self.cardidHex)+" "+str(self.nombre)+" "+str(self.apellido)

    class Meta:
        db_table = 'PersonalRegistrado'


class LiveData(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    cardidHex = models.CharField(max_length=8, null=False)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    empresa = models.CharField(max_length=50, null=True)
    cargo = models.CharField(max_length=50, null=True)
    f_ingreso = models.DateField(null=True)
    h_ingreso = models.TimeField(null=True)

    def __str__(self):
        return str(self.cardidHex)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'LiveData'


class Historial(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    cardidHex = models.CharField(max_length=8, null=False)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    empresa = models.CharField(max_length=50, null=True)
    cargo = models.CharField(max_length=50, null=True)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=2, null=False, default='0')

    def __str__(self):
        return str(self.cardidHex)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'Historial'


class NoRegistrados(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    cardidHex = models.CharField(max_length=8, null=True)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.cardidHex)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'NoRegistrados'


class deviceID(models.Model):
    id = models.IntegerField(primary_key=True)
    deviceID = models.CharField(max_length=8, null=True)
    ubicacion = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.deviceID)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'deviceID'


class UserInfo(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    DNI = models.CharField(max_length=8)
    Telefono = models.CharField(max_length=9)
    SegundoApellido = models.CharField(max_length=50)


#######################
