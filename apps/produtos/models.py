import os
import os
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.text import slugify
from django.utils.text import slugify

class MediaStorage(S3Boto3Storage):
    location = 'media/'
    location = 'media/'  # importante o /
    file_overwrite = False


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    categoria_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    dimensoes = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class ProdutoAtributo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="atributos")
    nome_atributo = models.CharField(max_length=255)
    valor_atributo = models.CharField(max_length=255)


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to='produtos/images', storage=MediaStorage())
    ordem = models.IntegerField(default=0)


def video_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    safe_name = slugify(base)
    return f'produtos/videos/{safe_name}{ext}'
    ordem = models.IntegerField(default=0)


def video_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    safe_name = slugify(base)
    return f'produtos/videos/{safe_name}{ext}'

class ProdutoVideo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to=video_upload_path, storage=MediaStorage())
    video = models.FileField(upload_to=video_upload_path, storage=MediaStorage())
    url_video = models.URLField()
    ordem = models.IntegerField(default=0)

    @property
    def url_video(self):
        return self.video.url if self.video else None

    @property
    def url_video(self):
        return self.video.url if self.video else None

    
    def __str__(self):
        return f"Vídeo {self.ordem} - {self.produto.nome}"
    