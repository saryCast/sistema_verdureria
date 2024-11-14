from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from web.models import *
from django.urls import reverse, reverse_lazy
from .forms import RegistroVentaForm, TotalVentasForm, StockForm
from django.utils import timezone

@login_required
def index(request):
    # Procesamiento del formulario de venta
    if request.method == "POST":
        form = RegistroVentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            
            # Verificar stock disponible
            if producto.stock < cantidad:
                ventas = Contiene.objects.filter(venta__user=request.user).select_related('producto', 'venta')
                return render(request, 'index.html', {
                    'form': form,
                    'ventas': ventas,
                    'error': 'No hay suficiente stock disponible.'
                })

            # Registrar la venta
            venta = Venta.objects.create(user=request.user, cantidad=cantidad, fecha=timezone.now(), producto=producto)
            Contiene.objects.create(venta=venta, producto=producto)
            producto.stock -= cantidad
            producto.save()

            return redirect('index')  # Redirigir para limpiar el formulario

    else:
        form = RegistroVentaForm()

    # Obtener todas las ventas del usuario actual
    ventas = Contiene.objects.filter(venta__user=request.user).select_related('producto', 'venta')
    return render(request, 'index.html', {'form': form, 'ventas': ventas})

@login_required
def ventas(request):
    # Procesamiento del formulario totalVentas
    if request.method == "POST":
        form = TotalVentasForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            fecha = form.cleaned_data['fecha']
            ventas = Contiene.objects.filter(venta__fecha=fecha, venta__producto=producto).select_related('producto', 'venta')
            return render(request, 'ventas.html', {'form': form, 'ventas': ventas})
    else:
        form = RegistroVentaForm()        
    # Obtener todas las ventas del usuario actual
    ventas = Contiene.objects.all().select_related('producto', 'venta')
    return render(request, 'ventas.html', {'form': form, 'ventas': ventas})


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request,'registration/register.html')
    
    def post(self, request):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2:
            messages.error(request,'passwords do not match')
            return redirect(reverse('register'))
        user=User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name)
         #user.is_active = False
        user.save()
        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('index')
class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Sesion Iniciada Exitosamente"
    template_name = 'registration/login.html'  
    redirect_authenticated_user = True
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, "Sesion Cerrada Exitosamente")
        return response
    
def stock(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            formato = form.cleaned_data['formato']

            try:
                cantidad_a_agregar = int(formato.cantidad)
            except ValueError:
                messages.error(request, 'Error: La cantidad del formato no es válida.')
                return redirect('stock')

            # Actualizar el stock en base al formato
            producto.stock += cantidad_a_agregar
            producto.save()

            # Mensaje de éxito
            messages.success(request, f'Se han añadido {cantidad_a_agregar} al stock de {producto.nombre} usando el formato {formato.nombre}.')
            return redirect('stock')
    else:
        form = StockForm()

    # Obtener todos los productos para mostrar el stock actual
        productos = Producto.objects.all()
        return render(request, 'stock.html', {'form': form, 'productos': productos})