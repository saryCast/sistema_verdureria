from django.urls import path
from . import views
from .views import index, CustomLoginView, CustomLogoutView, RegisterView, ventas, stock

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('ventas/', views.ventas, name='ventas'),
    path('stock/', views.stock, name='stock'),
]
