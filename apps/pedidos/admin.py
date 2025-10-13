from django.contrib import admin

from .models import PedidoItem, Produto, Entrega, Carrinho, CarrinhoItem

admin.site.register(PedidoItem)
admin.site.register(Produto)
admin.site.register(Entrega)
admin.site.register(Carrinho)
admin.site.register(CarrinhoItem)