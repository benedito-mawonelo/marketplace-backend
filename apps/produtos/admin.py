from django.contrib import admin

from .models import Categoria, Produto, ProdutoAtributo, ProdutoImagem, ProdutoVideo

admin.site.register(Categoria)
# admin.site.register(Produto)
admin.site.register(ProdutoAtributo)
admin.site.register(ProdutoImagem)
admin.site.register(ProdutoVideo)
