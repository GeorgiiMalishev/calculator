from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_file, name='export_excel'),
    path('calculate-fact/', views.calculate_fact, name='calculate_fact'),
    path('calculate-plan/', views.calculate_plan, name='calculate_plan'),
    path('calculator/<str:calculator_name>/', views.calculator_view, name='calculator_view')
]