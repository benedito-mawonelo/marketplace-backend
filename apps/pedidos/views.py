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
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Pedido.objects.filter(cliente=user).order_by('-data_pedido')

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
    permission_classes = [IsAuthenticated]
    

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
        Converte o carrinho em pedido
        """
        carrinho = get_object_or_404(Carrinho, user=request.user)
        socio_codigo = request.data.get("codigo_socio")

        if socio_codigo:
            try:
                socio = Socio.objects.get(codigo_socio=socio_codigo)
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
            pedido_item = PedidoItem.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )
            total += preco_unitario * quantidade

        desconto = 0
        if socio_codigo:
            desconto = total * Decimal(0.05)  # 5% desconto, exemplo
            Comissao.objects.create(
                socio=socio,
                pedido=pedido,
                valor=total * Decimal(0.02),  # comissão 2%, exemplo
                status="PENDENTE"
            )

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


class PedidoReciboView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        from .models import Pedido  # importa aqui para evitar problemas circulares
        try:
            pedido = Pedido.objects.get(pk=pk, cliente=request.user)
        except Pedido.DoesNotExist:
            return HttpResponse('Pedido não encontrado', status=404)

        # Logo servido pelo frontend (public/mawonelo-logo.png)
        frontend_origin = getattr(settings, 'FRONTEND_ORIGIN', 'http://localhost:3000')
        logo_url = f"{frontend_origin}/mawonelo-logo.png"

        itens_html = ''.join([
            f"<tr><td style='padding:8px 12px;border-bottom:1px solid #eee'>{it.quantidade} x {it.produto.nome}</td>"
            f"<td style='padding:8px 12px;text-align:right;border-bottom:1px solid #eee'>{it.preco_unitario} MZN</td></tr>"
            for it in pedido.itens.all()
        ])

        # Paleta verde e dourado
        green = '#16A34A'  # Verde
        gold = '#C9A227'   # Dourado
        dark = '#0F172A'

        html = f"""
        <html>
        <head>
          <meta charset='utf-8' />
          <title>Recibo do Pedido #{pedido.id}</title>
          <style>
            body {{ font-family: Arial, Helvetica, sans-serif; background:#f6f8fb; margin:0; padding:20px; color:{dark}; }}
            .container {{ max-width: 760px; margin: 0 auto; background:#fff; border-radius:12px; box-shadow:0 6px 20px rgba(0,0,0,0.08); overflow:hidden; }}
            .header {{ display:flex; align-items:center; justify-content:space-between; padding:20px 24px; background:{green}; color:#fff; }}
            .brand {{ display:flex; align-items:center; gap:12px; }}
            .brand img {{ height:42px; width:auto; border-radius:6px; background:#fff; padding:4px; }}
            .section {{ padding:20px 24px; }}
            .title {{ margin:0 0 6px 0; font-size:20px; color:{green}; }}
            .muted {{ color:#475569; margin:4px 0; }}
            .table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid #eef2f7; border-radius:8px; overflow:hidden; }}
            .totals {{ display:flex; justify-content:flex-end; gap:40px; margin-top:12px; }}
            .totals div {{ text-align:right; }}
            .total-amount {{ font-weight:700; color:{gold}; font-size:18px; }}
            .footer {{ padding:16px 24px; background:#F1F5F9; color:#475569; font-size:12px; text-align:center; }}
            .badge {{ display:inline-block; padding:2px 8px; border-radius:12px; background:{gold}; color:#111827; font-weight:700; font-size:12px; }}
            .meta {{ font-size:12px; opacity:0.9; }}
          </style>
        </head>
        <body>
          <div class='container'>
            <div class='header'>
              <div class='brand'>
                <img src='{logo_url}' alt='Logo' />
                <div>
                  <div style='font-weight:700; font-size:18px;'>Compra Fácil</div>
                  <div class='meta'>Recibo de compra</div>
                </div>
              </div>
              <div style='text-align:right;'>
                <div class='meta'>Pedido</div>
                <div style='font-weight:700; font-size:18px;'>#{pedido.id}</div>
                <div class='badge' style='margin-top:6px'>{pedido.status}</div>
              </div>
            </div>

            <div class='section'>
              <h3 class='title'>Dados do pedido</h3>
              <p class='muted'>Data: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')}</p>
              <p class='muted'>Cliente: {getattr(pedido.cliente, 'nome', pedido.cliente.email)}</p>
            </div>

            <div class='section'>
              <h3 class='title'>Itens</h3>
              <table class='table'>
                <thead>
                  <tr>
                    <th style='text-align:left; padding:10px 12px; background:#F8FAFC; border-bottom:1px solid #eee'>Produto</th>
                    <th style='text-align:right; padding:10px 12px; background:#F8FAFC; border-bottom:1px solid #eee'>Preço</th>
                  </tr>
                </thead>
                <tbody>
                  {itens_html}
                </tbody>
              </table>
              <div class='totals'>
                <div>
                  <div class='muted'>Total</div>
                  <div class='total-amount'>{pedido.total} MZN</div>
                </div>
              </div>
            </div>

            <div class='footer'>
              Obrigado pela sua compra! Guarde este recibo para referência. Compra Fácil © {pedido.data_pedido.strftime('%Y')}
            </div>
          </div>
        </body>
        </html>
        """

        response = HttpResponse(html, content_type="text/html; charset=utf-8")
        if request.GET.get('download'):
            filename = f"recibo-pedido-{pedido.id}.html"
            response['Content-Disposition'] = f"attachment; filename=\"{filename}\""
        return response