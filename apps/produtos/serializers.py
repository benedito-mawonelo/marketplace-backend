from rest_framework import serializers
from .models import Produto, ProdutoAtributo, ProdutoImagem, ProdutoVideo, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    atributos = serializers.StringRelatedField(many=True, read_only=True)
    imagens = serializers.StringRelatedField(many=True, read_only=True)
    videos = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

class ProdutoAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoAtributo
        fields = '__all__'

class ProdutoImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoImagem
        fields = '__all__'

class ProdutoVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoVideo
        fields = '__all__'
