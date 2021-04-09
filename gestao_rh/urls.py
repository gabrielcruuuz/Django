from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from gestao_rh import settings

from apps.funcionarios.API.views import FuncionarioViewSet
from apps.registro_hora_extra.API.views import HoraExtraViewSet

from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'api/funcionarios', FuncionarioViewSet)
routers.register(r'api/banco-horas', HoraExtraViewSet)


urlpatterns = [
    path('', include('apps.core.urls')),
    path('admin/', admin.site.urls),
    path('funcionarios/', include('apps.funcionarios.urls')),
    path('empresas/', include('apps.empresas.urls')),
    path('departamentos/', include('apps.departamentos.urls')),
    path('documentos/', include('apps.documentos.urls')),
    path('horas-extras/', include('apps.registro_hora_extra.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # ROTAS DA API
    url(r'^', include(routers.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
