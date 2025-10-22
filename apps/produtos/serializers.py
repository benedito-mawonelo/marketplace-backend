from rest_framework import serializers
from django.conf import settings
from urllib.parse import urlparse

try:
    import boto3
except Exception:  # boto3 pode não estar instalado em ambientes locais
    boto3 = None
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
    # Garante que sempre expomos uma URL utilizável do vídeo
    url_video = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProdutoVideo
        fields = '__all__'

    def get_url_video(self, obj):
        # 1) Tenta a URL padrão do storage (pode funcionar se o objeto/bucket for público)
        try:
            if obj and obj.video:
                url = obj.video.url
                if url:
                    return url
        except Exception:
            pass

        # 2) Se estiver em S3 privado, gera URL pré-assinada
        try:
            if not boto3 or not obj or not obj.video:
                return None

            bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
            region_name = getattr(settings, 'AWS_S3_REGION_NAME', None)
            aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
            aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

            # A chave do objeto no S3 normalmente é o caminho do arquivo no storage
            object_key = getattr(obj.video, 'name', None)
            if not bucket_name or not object_key:
                return None

            session = boto3.session.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
            s3_client = session.client('s3', region_name=region_name)
            presigned = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=getattr(settings, 'AWS_PRESIGNED_TTL', 3600),
            )
            return presigned
        except Exception:
            return None
        

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
