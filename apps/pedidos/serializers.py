from rest_framework import serializers
from .models import Carrinho, CarrinhoItem, Pedido, PedidoItem, Entrega
from apps.comissoes.models import Comissao
from apps.users.models import Socio

class CarrinhoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrinhoItem
        fields = '__all__'

class CarrinhoSerializer(serializers.ModelSerializer):
    itens = CarrinhoItemSerializer(many=True, read_only=True)
    class Meta:
        model = Carrinho
        fields = ['id', 'user', 'criado_em', 'itens']

class PedidoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItem
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = '__all__'

class ComissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comissao
        fields = '__all__'
