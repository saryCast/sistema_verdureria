from django.contrib import admin
from .models import Producto, Formato,Venta,Contiene, Categoria

# Register your models here.

admin.site.register(Producto)
admin.site.register(Formato)
admin.site.register(Venta)
admin.site.register(Contiene)
admin.site.register(Categoria)