# apps/produtos/models.py
from django.db import models

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
    url_imagem = models.URLField()
    ordem = models.IntegerField(default=0)


class ProdutoVideo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="videos")
    url_video = models.URLField()
