from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()
    unidades = models.BooleanField() 
    precio_por_unidad = models.IntegerField()
    categoria = models.ForeignKey(Categoria, null=True, blank=True, related_name='productos', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

class Formato(models.Model):
    nombre = models.CharField(max_length=45)
    cantidad = models.CharField(max_length=45)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.cantidad}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'cantidad: {self.cantidad} | producto: {self.producto.nombre} | Cliente: {self.user.username} | Fecha: {self.fecha}'

class Contiene(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)