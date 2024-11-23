import pytest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from myapp.models import Colaborador, Equipamento, Emprestimo


# Create your tests here.
def test_home_url():
    assert reverse('home') == '/'

def test_home_ok():
    client = Client()
    response = client.get(reverse('home'))
    assert response.status_code == 200

def test_home_template():
    client = Client()
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'listar.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_adicionar_colaborador():
    colaborador = Colaborador.objects.create(
        nome="Teste",
        data_nascimento="2000-01-01",
        email="sGw2e@example.com"
    )

    value = Colaborador.objects.get(id=colaborador.id)
    assert value.id == colaborador.id
    
@pytest.mark.django_db
def test_cadastrar__equipamento():
    equipamento = Equipamento.objects.create(
        nome="Teste",
        tipo="Teste",
        quantidade=10
    )

    value = Equipamento.objects.get(id=equipamento.id)
    assert value.id == equipamento.id

@pytest.mark.django_db
def test_cadastrar_emprestimo():
    emprestimo = Emprestimo.objects.create(
        data_emprestimo="2023-01-01",
        data_prevista_devolucao="2023-01-02",
        colaborador=Colaborador.objects.create(
            nome="Teste",
            data_nascimento="2000-01-01",
            email="sGw2e@example.com"
        ),
        equipamento=Equipamento.objects.create(
            nome="Teste",
            tipo="Teste",
            quantidade=10
        ),
        quantidade_equipamento=1,
        observacao="Teste",
        status=True
    )

    value = Emprestimo.objects.get(id=emprestimo.id)
    assert value.id == emprestimo.id

@pytest.mark.django_db
def test_atualizar_emprestimo():
    emprestimo = Emprestimo.objects.create(
        data_emprestimo="2023-01-01",
        data_prevista_devolucao="2023-01-02",
        colaborador=Colaborador.objects.create(
            nome="Teste",
            data_nascimento="2000-01-01",
            email="sGw2e@example.com"
        ),
        equipamento=Equipamento.objects.create(
            nome="Teste",
            tipo="Teste",
            quantidade=10
        ),
        quantidade_equipamento=1,
        observacao="Teste",
        status=True
    )

    emprestimo.data_devolucao = "2023-01-03"
    emprestimo.save()

    value = Emprestimo.objects.get(id=emprestimo.id)
    assert value.data_devolucao == "2023-01-03"

