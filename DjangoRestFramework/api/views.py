from rest_framework import viewsets
from .serializer import (
    ClaseSerializer, MateriaSerializer, UsuarioSerializer, TranscripcionSerializer, ResumenSerializer)
from .models import (Clase, Materia, Usuario, Transcripcion, Resumen)
from rest_framework.response import Response
from rest_framework.decorators import action
from openai import OpenAI
import tiktoken
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os
# Create your views here.
client = OpenAI(
    # this is also the default, it can be omitted
    api_key="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",
)


# video_path = os.path.abspath("C:/Users/estar/OneDrive/Escritorio/proyectos/DjangoRestFrameworkPriv/video.mp4")
video_path = os.path.abspath("video.mp4")
# audio_path = os.path.abspath("C:/Users/estar/OneDrive/Escritorio/proyectos/DjangoRestFrameworkPriv/audio.mp3")
audio_path = os.path.abspath("audio.mp3")


def extraer_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)

    audio_clip = video_clip.audio

    audio_clip.write_audiofile(audio_path, codec='mp3', bitrate='16k')

    audio_clip.close()
    video_clip.close()


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            correo = request.data.get('correo')
            contrasenia = request.data.get('contrasenia')
            try:
                user_obj = Usuario.objects.get(
                    correo=correo, password=contrasenia)
                serializer = UsuarioSerializer(user_obj)
                return Response(serializer.data)
            except Usuario.DoesNotExist:
                return Response({'mensaje': 'Usuario no encontrado'}, status=404)

        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class TranscriptionViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def transcription(self, request):
        try:
            id_video = request.data.get('id_video')
            language = request.data.get('language')
            try:
                url = 'https://www.youtube.com/watch?v='+id_video
                youtube = YouTube(url)
                video = youtube.streams.get_lowest_resolution()
                video.download(filename="video.mp4")
                extraer_audio(video_path, audio_path)

                # Utiliza el bloque with para asegurarte de que el archivo se cierre
                with open(audio_path, "rb") as audio_file:
                    result = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )

                texto_transcrito = result.text
                prompt = f""" Translate the following text to {
                    language}, ensuring that the translation accurately conveys the original meaning. Pay attention to nuances and context, and provide a clear and coherent {language} rendition of the content. """
                request = prompt + texto_transcrito
                modelTokens = ''
                enc = tiktoken.encoding_for_model('gpt-3.5-turbo')
                if len(enc.encode(request)) < 4097:
                    modelTokens = 'gpt-3.5-turbo'
                else:
                    modelTokens = 'gpt-3.5-turbo-16k'
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": request,
                        }
                    ],
                    model=modelTokens,
                    stream=True,
                )
                response = ''
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                datos_transcripcion = {
                    "transcripcion": response
                }
                os.remove(video_path)
                os.remove(audio_path)
                return Response(datos_transcripcion)
            except Exception as e:
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return Response({'mensaje': f'Problemas al generar transcripción - {str(e)}'}, status=500)
        except KeyError:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class SummaryViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def summary(self, request):
        try:
            message = request.data.get('message')
            language = request.data.get('language')
            try:
                prompt = f""" Utilizing your summarization skills, distill key insights and main points from the following text into a concise yet comprehensive summary. Focus on capturing essential ideas while minimizing unnecessary details. You must translate the summary into {
                    language}. """
                request = prompt + message
                modelTokens = ''
                enc = tiktoken.encoding_for_model('gpt-3.5-turbo')
                if len(enc.encode(request)) < 4097:
                    modelTokens = 'gpt-3.5-turbo'
                else:
                    modelTokens = 'gpt-3.5-turbo-16k'
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": request,
                        }
                    ],
                    model=modelTokens,
                    stream=True,
                )
                response = ''
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                datos_resumen = {
                    "message": response
                }
                return Response(datos_resumen)
            except:
                return Response({'mensaje': 'Problemas al generar resumen'}, status=500)
        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class TranslateViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def translate(self, request):
        try:
            message = request.data.get('message')
            language = request.data.get('language')
            try:
                prompt = f""" Translate the following text to {
                    language}, ensuring that the translation accurately conveys the original meaning. Pay attention to nuances and context, and provide a clear and coherent {language} rendition of the content. """
                request = prompt + message
                modelTokens = ''
                enc = tiktoken.encoding_for_model('gpt-3.5-turbo')
                if len(enc.encode(request)) < 4097:
                    modelTokens = 'gpt-3.5-turbo'
                else:
                    modelTokens = 'gpt-3.5-turbo-16k'
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": request,
                        }
                    ],
                    model=modelTokens,
                    stream=True,
                )
                response = ''
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                datos_resumen = {
                    "message": response
                }
                return Response(datos_resumen)
            except:
                return Response({'mensaje': 'Problemas al generar resumen'}, status=500)
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
                    materias = Materia.objects.all()
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
            docente = request.data.get('docente')
            if ci % 2 == 0:
                semestre = 9
            try:
                if docente:
                    clases = Clase.objects.all()
                    serializer = ClaseSerializer(clases, many=True)
                    return Response(serializer.data)
                clases = Clase.objects.filter(semestre=semestre)
                serializer = ClaseSerializer(clases, many=True)
                return Response(serializer.data)
            except Clase.DoesNotExist:
                return Response({'mensaje': 'Clases no encontradas'}, status=404)

        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)
    
    @action(detail=False, methods=['post'])
    def clasesMateria(self, request):
        try:
            id_materia = request.data.get('id_materia')
            try:
                clases = Clase.objects.filter(id_materia=id_materia)
                serializer = ClaseSerializer(clases, many=True)
                return Response(serializer.data)
            except Clase.DoesNotExist:
                return Response({'mensaje': 'Clases no encontradas'}, status=404)
        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class TranscripcionesViewSet(viewsets.ModelViewSet):
    queryset = Transcripcion.objects.all()
    serializer_class = TranscripcionSerializer

    @action(detail=False, methods=['post'])
    def TranscripcionExistente(self, request):
        try:
            id_clase = request.data.get('id_clase')
            language = request.data.get('language')
            try:
                transcripcion = Transcripcion.objects.get(
                    id_clase=id_clase, language=language)
                serializer = TranscripcionSerializer(transcripcion)
                return Response(serializer.data)
            except Transcripcion.DoesNotExist:
                return Response({'mensaje': 'Transcripcion no encontrada'}, status=404)
        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)


class ResumenesViewSet(viewsets.ModelViewSet):
    queryset = Resumen.objects.all()
    serializer_class = ResumenSerializer

    @action(detail=False, methods=['post'])
    def ResumenExistente(self, request):
        try:
            id_clase = request.data.get('id_clase')
            language = request.data.get('language')
            try:
                resumen = Resumen.objects.get(
                    id_clase=id_clase, language=language)
                serializer = ResumenSerializer(resumen)
                return Response(serializer.data)
            except Resumen.DoesNotExist:
                return Response({'mensaje': 'Resumen no encontrado'}, status=404)
        except KeyError:
            return Response({'mensaje': 'Parámetros incorrectos'}, status=400)
