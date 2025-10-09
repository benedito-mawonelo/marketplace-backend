from rest_framework import viewsets
from .models import Produto, ProdutoAtributo, ProdutoImagem, ProdutoVideo, Categoria
from .serializers import (
    ProdutoSerializer, ProdutoAtributoSerializer, ProdutoImagemSerializer,
    ProdutoVideoSerializer, CategoriaSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ProdutoAtributoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoAtributo.objects.all()
    serializer_class = ProdutoAtributoSerializer

class ProdutoImagemViewSet(viewsets.ModelViewSet):
    queryset = ProdutoImagem.objects.all()
    serializer_class = ProdutoImagemSerializer

class ProdutoVideoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoVideo.objects.all()
    serializer_class = ProdutoVideoSerializer
