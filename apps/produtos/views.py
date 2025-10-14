from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Produto, ProdutoAtributo, ProdutoImagem, ProdutoVideo, Categoria
from .serializers import (
    ProdutoSerializer, ProdutoAtributoSerializer, ProdutoImagemSerializer,
    ProdutoVideoSerializer, CategoriaSerializer
)

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated and getattr(user, 'role', '') == 'ADMIN')


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdminRole()]
        return []

class ProdutoAtributoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoAtributo.objects.all()
    serializer_class = ProdutoAtributoSerializer

class ProdutoImagemViewSet(viewsets.ModelViewSet):
    queryset = ProdutoImagem.objects.all()
    serializer_class = ProdutoImagemSerializer

class ProdutoVideoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoVideo.objects.all()
    serializer_class = ProdutoVideoSerializer
