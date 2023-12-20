from rest_framework import viewsets
from .serializer import (ClaseSerializer, MateriaSerializer, ProgrammerSerializer, UsuarioSerializer)
from .models import (Clase, Materia, Programmer, Usuario)

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            correo = request.data.get('correo')
            contrasenia = request.data.get('contrasenia')
            try:
                user_obj = Usuario.objects.get(correo=correo, password=contrasenia)
                serializer = UsuarioSerializer(user_obj)
                return Response(serializer.data)
            except Usuario.DoesNotExist:
                return Response({'mensaje': 'Usuario no encontrado'}, status=404)

        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)

class MateriasViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

    @action(detail=False, methods=['post'])
    def materiasImpar(self, request):
        try:
            semestre = 10
            ci = request.data.get('ci')
            docente = request.data.get('docente')
            if ci % 2 == 0:
                semestre = 9
            try:
                if docente:
                    materias = Materia.objects.filter(is_docente=True)
                    serializer = MateriaSerializer(materias, many=True)
                    return Response(serializer.data)
                materias = Materia.objects.filter(semestre=semestre)
                serializer = MateriaSerializer(materias, many=True)
                return Response(serializer.data)
            except Materia.DoesNotExist:
                return Response({'mensaje': 'Materias no encontradas'}, status=404)

        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class ClasesViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

    @action(detail=False, methods=['post'])
    def clasesImpar(self, request):
        try:
            semestre = 10
            ci = request.data.get('ci')
            if ci % 2 == 0:
                semestre = 9
            try:
                clases = Clase.objects.filter(semestre=semestre)
                serializer = ClaseSerializer(clases, many=True)
                return Response(serializer.data)
            except Clase.DoesNotExist:
                return Response({'mensaje': 'Clases no encontradas'}, status=404)

        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)
