from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Cria um produto com todos os dados relacionados em uma única requisição
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def upload_imagem(self, request, pk=None):
        # Mantém o upload individual para adicionar depois
        produto = self.get_object()
        imagem = request.FILES.get('imagem')
        ordem = request.data.get('ordem', 0)
        
        if imagem:
            produto_imagem = ProdutoImagem.objects.create(
                produto=produto,
                imagem=imagem,
                ordem=ordem
            )
            serializer = ProdutoImagemSerializer(produto_imagem)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Nenhuma imagem fornecida'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def upload_video(self, request, pk=None):
        # Mantém o upload individual
        produto = self.get_object()
        video = request.FILES.get('video')
        ordem = request.data.get('ordem', 0)
        
        if video:
            produto_video = ProdutoVideo.objects.create(
                produto=produto,
                video=video,
                ordem=ordem
            )
            serializer = ProdutoVideoSerializer(produto_video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Nenhum vídeo fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    
class ProdutoAtributoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoAtributo.objects.all()
    serializer_class = ProdutoAtributoSerializer

class ProdutoImagemViewSet(viewsets.ModelViewSet):
    queryset = ProdutoImagem.objects.all()
    serializer_class = ProdutoImagemSerializer

class ProdutoVideoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoVideo.objects.all()
    serializer_class = ProdutoVideoSerializer