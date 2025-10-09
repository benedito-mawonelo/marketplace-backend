# apps/pedidos/models.py
from django.db import models
from apps.users.models import User, Socio
from apps.produtos.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("ENVIADO", "Enviado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado"),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class Entrega(models.Model):
    ESTADO_CHOICES = [
        ("PREPARACAO", "Preparação"),
        ("A_CAMINHO", "A Caminho"),
        ("ENTREGUE", "Entregue"),
        ("DEVOLVIDO", "Devolvido"),
    ]
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="entrega")
    transportadora = models.CharField(max_length=255)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="PREPARACAO")
    data_envio = models.DateTimeField(null=True, blank=True)
    data_entrega = models.DateTimeField(null=True, blank=True)



class Carrinho(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrinho")
    criado_em = models.DateTimeField(auto_now_add=True)

class CarrinhoItem(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrinho', 'produto')
