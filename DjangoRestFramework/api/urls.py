from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuariosViewSet)
router.register(r'materias', views.MateriasViewSet)
router.register(r'clases', views.ClasesViewSet)
router.register(r'transcripciones', views.TranscripcionesViewSet)
router.register(r'resumenes', views.ResumenesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'usuarios/login/',
        views.UsuariosViewSet.as_view({'post': 'login'}), name='login'
    ),
    path(
        'whisper/resumen/',
        views.SummaryViewSet.as_view({'post': 'summary'}), name='summary'
    ),
    path(
        'whisper/transcripcion/',
        views.TranscriptionViewSet.as_view({'post': 'transcription'}), name='transcription'
    ),
    path(
        'materias/materiasImpar/',
        views.MateriasViewSet.as_view({'post': 'materiasImpar'}), name='materiasImpar'
    ),
    path(
        'clases/clasesImpar/',
        views.ClasesViewSet.as_view({'post': 'clasesImpar'}), name='clasesImpar'
    ),
    path(
        'clases/clasesMateria/',
        views.ClasesViewSet.as_view({'post': 'clasesMateria'}), name='clasesMateria'
    ),
    path(
        'transcripcionesExistente/',
        views.TranscripcionesViewSet.as_view({'post': 'TranscripcionExistente'}), name='TranscripcionExistente'
    ),
    path(
        'resumenesExistente/',
        views.ResumenesViewSet.as_view({'post': 'ResumenExistente'}), name='ResumenExistente'
    ),
    path(
        'traducir/',
        views.TranslateViewSet.as_view({'post': 'translate'}), name='translate'
    ),
]
