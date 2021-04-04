from django.urls import path
from .views import (
    HoraExtraList
    , HoraExtraEdit
    , HoraExtraEditBase
    , UsouHoraExtra
    , NaoUsouHoraExtra
    , HoraExtraDelete
    , HoraExtraCreate
    , ExportarExcel)

urlpatterns = [
    path('', HoraExtraList.as_view(), name="list_hora_extra"),
    path('editar/<int:pk>/', HoraExtraEditBase.as_view(), name="update_hora_extra_base"),
    path('editar-funcionario/<int:pk>/', HoraExtraEdit.as_view(), name="update_hora_extra"),
    path('usou-hora-extra/<int:pk>/', UsouHoraExtra.as_view(), name="usou_hora_extra"),
    path('nao-usou-hora-extra/<int:pk>/', NaoUsouHoraExtra.as_view(), name="nao_usou_hora_extra"),
    path('deletar/<int:pk>/', HoraExtraDelete.as_view(), name="delete_hora_extra"),
    path('novo', HoraExtraCreate.as_view(), name="create_hora_extra"),
    path('exportar-excel', ExportarExcel.as_view(), name="exportar_excel"),

]
