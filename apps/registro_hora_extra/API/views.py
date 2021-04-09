from rest_framework import viewsets
from apps.registro_hora_extra.API.serializers import HoraExtraSerializer
from apps.registro_hora_extra.models import RegistroHoraExtra
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class HoraExtraViewSet(viewsets.ModelViewSet):
    queryset = RegistroHoraExtra.objects.all()
    serializer_class = HoraExtraSerializer
    # USANDO AUTENTICAÇÃO VIA TOKEN
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)