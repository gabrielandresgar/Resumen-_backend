from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'programmers', views.ProgrammerViewSet)
router.register(r'usuarios', views.UsuariosViewSet)
router.register(r'materias', views.MateriasViewSet)
router.register(r'clases', views.ClasesViewSet)
urlpatterns = [
    path(
        '', include(router.urls)
    ),
    path(
        'usuarios/login/', views.UsuariosViewSet.as_view({'post': 'login'}), name='login'
    ),
    path(
        'materias/materiasImpar/',
        views.MateriasViewSet.as_view({'post': 'materiasImpar'}), name='materiasImpar'
    ),
    path(
        'clases/clasesImpar/',
        views.ClasesViewSet.as_view({'post': 'clasesImpar'}), name='clasesImpar'
    ),
]
