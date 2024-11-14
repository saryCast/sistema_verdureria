from django import forms
from .models import Producto, Formato, Venta, Contiene

class RegistroVentaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label='Producto',required=False)
    cantidad = forms.IntegerField(min_value=1,required=False, label="Cantidad", widget=forms.NumberInput(attrs={'placeholder': 'Ingrese Cantidad'}))

class TotalVentasForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label='Producto',required=False)
    fecha=forms.DateField(required=False,label="Fecha", widget=forms.DateInput(attrs={'placeholder': 'Seleccione Fecha','type': 'date' }))

class StockForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label='Producto')
    formato = forms.ModelChoiceField(queryset=Formato.objects.all(), empty_label='Formato')