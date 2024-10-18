from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect
from myapp.models import Colaborador, Equipamento, Emprestimo
from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.
from django.shortcuts import render
from .models import Emprestimo, Colaborador, Equipamento

def listar_emprestimo(request):
    nome = request.GET.get('nome', '').strip()  # Pega o valor da pesquisa

    # Usar select_related para otimizar consultas
    if nome:
        # Filtra empréstimos com base no nome do equipamento ou colaborador
        values = Emprestimo.objects.select_related('colaborador', 'equipamento').filter(
            equipamento__nome__icontains=nome
        ) | Emprestimo.objects.select_related('colaborador', 'equipamento').filter(
            colaborador__nome__icontains=nome
        )
        
        # Filtra equipamentos com base no nome
        values_equipamentos = Equipamento.objects.filter(
            nome__icontains=nome
        )
    else:
        values = Emprestimo.objects.select_related('colaborador', 'equipamento').all()
        values_equipamentos = Equipamento.objects.all()

    # Processa os empréstimos filtrados
    emprestimos = []
    for value in values:
        emprestimo = {
            'id': value.id,
            'data_emprestimo': value.data_emprestimo,
            'data_devolucao': value.data_devolucao,
            'colaborador': value.colaborador.nome,  # Objeto completo já obtido por select_related
            'equipamento': value.equipamento.nome,  # Objeto completo já obtido por select_related
            'quantidade_equipamento': value.quantidade_equipamento,
            'status': 'Emprestado' if value.status else 'Devolvido',
        }
        emprestimos.append(emprestimo)

    # Processa os equipamentos filtrados
    equipamentos = []
    for value in values_equipamentos:
        equipamento = {
            'id': value.id,
            'nome': value.nome,
            'tipo': value.tipo,
            'quantidade': value.quantidade,
        }
        equipamentos.append(equipamento)

    context = {
        'lista_emprestimo': emprestimos,
        'lista_equipamentos': equipamentos
    }
    return render(request, 'myapp/pages/listar.html', context)

@login_required(login_url='/login/login/')
@permission_required('myapp.criar_colaboradores',login_url='/login/login/', raise_exception=True)
def criar_colaborador(request):
    nome = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')  # Captura a data de nascimento
        email = request.POST.get('email')
        
        if nome and data_nascimento and email:
            # Cria o colaborador com a data de nascimento
            Colaborador.objects.create(nome=nome, data_nascimento=data_nascimento, email=email)
            return redirect(listar_emprestimo)
    
    return render(request, 'myapp/pages/cadastrar_colaborador.html', {"ultimo_nome": nome})

@login_required(login_url='/login/login/')
@permission_required('myapp.criar_equipamentos',login_url='/login/login/', raise_exception=True)
def criar_equipamento(request):
    nome = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        quantidade = request.POST.get('quantidade')
        if nome and tipo and quantidade:
            Equipamento.objects.create(nome=nome, tipo=tipo, quantidade=quantidade)
            return redirect(listar_emprestimo)
    return render(request, 'myapp/pages/cadastrar_equipamento.html', {"ultimo_nome": nome})

@login_required(login_url='/login/login/')
@permission_required('myapp.atualizar_equipamentos' ,login_url='/login/login/', raise_exception=True)
def atualizar_equipamento(request, id):
    item = Equipamento.objects.get(id=id)
    if request.method == 'POST':
        itemNome = request.POST.get('nome')
        itemTipo = request.POST.get('tipo')
        itemQuantidade_str = request.POST.get('quantidade')  # Captura a quantidade como string

        # Verifica se todos os campos estão preenchidos
        if itemNome and itemTipo and itemQuantidade_str:
            try:
                itemQuantidade = int(itemQuantidade_str)  # Converte a quantidade para inteiro
            except ValueError:
                return render(request, 'myapp/pages/atualizar_equipamento.html', {
                    "item": item,
                    "erro": "A quantidade deve ser um número válido."
                })

            # Atualiza os atributos do item
            item.nome = itemNome
            item.tipo = itemTipo  # Atribuição correta do tipo
            item.quantidade = itemQuantidade  # Atribuição correta da quantidade
            item.save()  # Salva as alterações no banco de dados

            return redirect(listar_emprestimo)  # Redireciona para a lista de empréstimos
        else:
            return render(request, 'myapp/pages/atualizar_equipamento.html', {
                "item": item,
                "erro": "Por favor, preencha todos os campos."
            })

    return render(request, 'myapp/pages/atualizar_equipamento.html', {"item": item})

@login_required(login_url='/login/login/')
@permission_required('myapp.deletar_equipamentos',login_url='/login/login/', raise_exception=True)
def deletar_equipamento(request, id):
    item = Equipamento.objects.get(id=id)
    item.delete()
    return redirect(listar_emprestimo)

@login_required(login_url='/login/login/')
@permission_required('myapp.criar_emprestimos',login_url='/login/login/', raise_exception=True)
def criar_emprestimo(request):
    colaboradores = None
    equipamentos = None
    
    if request.method == 'GET':
        colaboradores = Colaborador.objects.all()
        equipamentos = Equipamento.objects.all()
        return render(request, 'myapp/pages/cadastrar_emprestimo.html', {"colaboradores": colaboradores, "equipamentos": equipamentos})

    elif request.method == 'POST':
        data_emprestimo = request.POST.get('data_emprestimo')
        data_devolucao = request.POST.get('data_devolucao')
        colaborador = request.POST.get('colaborador')
        equipamento = request.POST.get('equipamento')
        quantidade_equipamento_str = request.POST.get('quantidade_equipamento')
        status_str = request.POST.get('status')

        messages = []  # Lista para armazenar mensagens de erro

        # Verifica se a quantidade foi fornecida
        if not quantidade_equipamento_str:
            messages.append("Por favor, forneça a quantidade de equipamentos.")
        else:
            # Converte para inteiro e verifica se a conversão foi bem-sucedida
            try:
                quantidade_equipamento = int(quantidade_equipamento_str)
            except ValueError:
                messages.append("Quantidade deve ser um número válido.")
                quantidade_equipamento = 0

        # Verifica se a data de devolução não é anterior à data de empréstimo
        if data_emprestimo >= data_devolucao: 
            messages.append("A data de devolução não pode ser anterior à data de empréstimo.")

        # Obtém a quantidade do equipamento disponível
        equipamento_obj = Equipamento.objects.get(id=equipamento)
        qnt_equipamento_db = equipamento_obj.quantidade
        
        # Verifica se a quantidade desejada é maior que a disponível
        if quantidade_equipamento > qnt_equipamento_db:
            messages.append("Quantidade de equipamentos insuficientes.")

        # Se houver mensagens de erro, renderiza a página novamente com mensagens
        if messages:
            colaboradores = Colaborador.objects.all()  # Recarrega os colaboradores
            equipamentos = Equipamento.objects.all()  # Recarrega os equipamentos
            return render(request, 'myapp/pages/cadastrar_emprestimo.html', {
                "colaboradores": colaboradores,
                "equipamentos": equipamentos,
                "messages": messages
            })

        # Converte o status de string para booleano
        status = status_str == "Emprestado"

        # Cria o empréstimo
        emprestimo = Emprestimo.objects.create(
            data_emprestimo=data_emprestimo,
            data_devolucao=data_devolucao,
            colaborador_id=colaborador,
            equipamento_id=equipamento,
            status=status,
            quantidade_equipamento=quantidade_equipamento
        )

        # Atualiza a quantidade do equipamento
        if status:  # se for Emprestado
            equipamento_obj.quantidade -= quantidade_equipamento
        else:  # se for Devolvido
            equipamento_obj.quantidade += quantidade_equipamento
        
        # Salva as alterações no equipamento
        equipamento_obj.save()
        
        return redirect(listar_emprestimo)

    return render(request, 'myapp/pages/cadastrar_emprestimo.html', {"colaboradores": colaboradores, "equipamentos": equipamentos})

@login_required(login_url='/login/login/')
@permission_required('myapp.atualizar_emprestimos',login_url='/login/login/', raise_exception=True)
def atualizar_emprestimo(request, id):
    emprestimo = Emprestimo.objects.get(id=id)
    equipamento = emprestimo.equipamento  # Obtém o equipamento associado ao empréstimo

    if request.method == 'POST':
        status = request.POST.get('status')

        # Verifica se o status foi fornecido
        if status is not None:
            # Ajuste a quantidade de equipamentos com base no status anterior e no novo status
            if emprestimo.status:  # Status atual é 'Emprestado'
                if status == 'Devolvido':
                    # Se está mudando para 'Devolvido', aumenta a quantidade
                    equipamento.quantidade += emprestimo.quantidade_equipamento
            else:  # Status atual é 'Devolvido'
                if status == 'Emprestado':
                    # Se está mudando para 'Emprestado', diminui a quantidade
                    equipamento.quantidade -= emprestimo.quantidade_equipamento

            # Atualiza o status do empréstimo
            emprestimo.status = (status == 'Emprestado')  # Converte o status para booleano
            
            # Salva as alterações no empréstimo e no equipamento
            emprestimo.save()
            equipamento.save()

            return redirect(listar_emprestimo)  # Redireciona para a lista de empréstimos
        else:
            return render(request, 'myapp/pages/atualizar_emprestimo.html', {
                "item": emprestimo,
                "erro": "Por favor, selecione um status."
            })

    return render(request, 'myapp/pages/atualizar_emprestimo.html', {"item": emprestimo})

def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    nome = request.GET.get('nome')
    print("aleluia")
    if nome:
        colaboradores = colaboradores.filter(nome__icontains=nome)

    return colaboradores


def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    nome = request.GET.get('nome')
    if nome:
        equipamentos = equipamentos.filter(nome__icontains=nome)

    return render(request, 'myapp/pages/listar.html', {"equipamentos": equipamentos})
