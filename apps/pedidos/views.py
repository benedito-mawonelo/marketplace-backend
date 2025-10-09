from .serializers import PedidoSerializer, PedidoItemSerializer, EntregaSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Carrinho, CarrinhoItem, Pedido, PedidoItem, Entrega
from apps.comissoes.models import Comissao
from .serializers import CarrinhoSerializer, PedidoSerializer, EntregaSerializer
from django.shortcuts import get_object_or_404
from apps.users.models import Socio
from decimal import Decimal

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.all()
    serializer_class = PedidoItemSerializer

class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer




class CarrinhoViewSet(viewsets.ViewSet):
    """
    CRUD de carrinho e conversão para pedido
    """

    def list(self, request):
        carrinho, created = Carrinho.objects.get_or_create(user=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def adicionar_item(self, request):
        carrinho, _ = Carrinho.objects.get_or_create(user=request.user)
        produto_id = request.data.get("produto_id")
        quantidade = int(request.data.get("quantidade", 1))

        item, created = CarrinhoItem.objects.get_or_create(
            carrinho=carrinho, produto_id=produto_id,
            defaults={'quantidade': quantidade}
        )
        if not created:
            item.quantidade += quantidade
            item.save()
        return Response({"message": "Produto adicionado ao carrinho."})

    @action(detail=False, methods=['post'])
    def remover_item(self, request):
        carrinho = get_object_or_404(Carrinho, user=request.user)
        produto_id = request.data.get("produto_id")
        CarrinhoItem.objects.filter(carrinho=carrinho, produto_id=produto_id).delete()
        return Response({"message": "Produto removido."})

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Converte o carrinho em Pedido
        """
        carrinho = get_object_or_404(Carrinho, user=request.user)
        socio_codigo = request.data.get("codigo_socio")
        if socio_codigo:
            try: 
                Socio.objects.get(codigo_socio=socio_codigo)
            except Socio.DoesNotExist:
                return Response({"error": "Código de sócio inválido"}, status=400)


        pedido = Pedido.objects.create(
            cliente=request.user,
            total=0,  # calcularemos abaixo
            status="PENDENTE"
        )

        total = 0
        for item in carrinho.itens.all():
            preco_unitario = item.produto.preco
            quantidade = Decimal(item.quantidade)  # <- converte para Decimal
            PedidoItem.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )
            total += preco_unitario * quantidade


        desconto = 0
        if socio_codigo:
            try:
                socio = Socio.objects.get(codigo_socio=socio_codigo)
                desconto = total * Decimal(0.05)  # 5% desconto, exemplo
                Comissao.objects.create(
                    socio=socio,
                    pedido=pedido,
                    valor=total * Decimal(0.02),  # comissão 2%, exemplo
                    status="PENDENTE"
                )
            except Socio.DoesNotExist:
                pass

        pedido.total = total - desconto
        pedido.save()

        # limpar carrinho
        carrinho.itens.all().delete()

        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    @action(detail=True, methods=['post'])
    def confirmar_pagamento(self, request, pk=None):
        pedido = self.get_object()
        pedido.status = "PAGO"
        pedido.save()

        # cria entrega
        Entrega.objects.create(
            pedido=pedido,
            transportadora="YANGO",
            estado="PREPARACAO"
        )

        return Response({"message": "Pagamento confirmado e entrega criada."})


class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer

    @action(detail=True, methods=['post'])
    def atualizar_estado(self, request, pk=None):
        entrega = self.get_object()
        novo_estado = request.data.get("estado")
        entrega.estado = novo_estado
        entrega.save()
        return Response({"message": f"Entrega atualizada para {novo_estado}"})
