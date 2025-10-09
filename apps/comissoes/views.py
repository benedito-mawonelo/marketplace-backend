from rest_framework import viewsets
from .models import Comissao
from .serializers import ComissaoSerializer

class ComissaoViewSet(viewsets.ModelViewSet):
    queryset = Comissao.objects.all()
    serializer_class = ComissaoSerializer
