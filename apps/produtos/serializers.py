from rest_framework import serializers
from .models import Produto, ProdutoAtributo, ProdutoImagem, ProdutoVideo, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
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
        

class ProdutoSerializer(serializers.ModelSerializer):
    atributos = ProdutoAtributoSerializer(many=True, required=False)
    imagens = ProdutoImagemSerializer(many=True, required=False)
    videos = ProdutoVideoSerializer(many=True, required=False)
    
    class Meta:
        model = Produto
        fields = '__all__'

    def create(self, validated_data):
        # Extrai os dados relacionados
        atributos_data = validated_data.pop('atributos', [])
        imagens_data = validated_data.pop('imagens', [])
        videos_data = validated_data.pop('videos', [])
        
        # Cria o produto
        produto = Produto.objects.create(**validated_data)
        
        # Cria os atributos
        for atributo_data in atributos_data:
            ProdutoAtributo.objects.create(produto=produto, **atributo_data)
        
        # Cria as imagens
        for imagem_data in imagens_data:
            ProdutoImagem.objects.create(produto=produto, **imagem_data)
        
        # Cria os vídeos
        for video_data in videos_data:
            ProdutoVideo.objects.create(produto=produto, **video_data)
        
        return produto
