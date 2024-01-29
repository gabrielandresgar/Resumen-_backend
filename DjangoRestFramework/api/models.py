from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, contrasenia=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(contrasenia)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, contrasenia=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo, contrasenia, **extra_fields)


class Usuario(AbstractBaseUser):
    cedula = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    tipoUsuario = models.CharField(max_length=1)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['cedula']

    def __str__(self):
        return self.correo


class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    semestre = models.PositiveSmallIntegerField()
    is_docente = models.BooleanField(default=False)


class Clase(models.Model):
    id_materia = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    id_video = models.CharField(max_length=100)
    semestre = models.PositiveSmallIntegerField()


class Transcripcion(models.Model):
    id_clase = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=50)
    Message = models.TextField()

class Resumen(models.Model):
    id_clase = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=50)
    Message = models.TextField()