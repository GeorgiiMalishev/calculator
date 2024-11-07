from django.urls import path
from . import views

urlpatterns = [
    path('calculator/', views.calculator_view, name='calculator'),  # Путь к HTML странице
    path('calculate/', views.calculate, name='calculate'),  # Путь для выполнения расчетов (должен быть уже настроен)
]