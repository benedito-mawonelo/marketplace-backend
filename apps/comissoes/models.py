# apps/comissoes/models.py
from django.db import models
from apps.pedidos.models import Pedido
from apps.users.models import Socio

class Comissao(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
    ]
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="comissoes")
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="comissoes")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")
