from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adicionar/', views.criar_colaborador, name='criar_colaborador'),
    path('criar_equipamento/', views.criar_equipamento, name='criar_equipamento'),
    path('emprestimo/', views.criar_emprestimo, name='emprestimo'),
    path('atualizar/<int:id>/', views.atualizar_emprestimo, name='atualizar_emprestimo'),
    path('atualizar_equipamento/<int:id>/', views.atualizar_equipamento, name='atualizar_equipamento'),
    path('deletar_equipamento/<int:id>/', views.deletar_equipamento, name='deletar_equipamento'),
       
]