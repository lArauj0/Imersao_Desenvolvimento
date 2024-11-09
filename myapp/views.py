from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect
from myapp.models import Colaborador, Equipamento, Emprestimo
from django.contrib.auth.decorators import login_required, permission_required


def listar_emprestimo(request):
    nome = request.GET.get('nome', '').strip()
    status = request.GET.get('status', '').strip()
      # Pega o valor da pesquisa

    values_colaboradores = []
    values_equipamentos = []
    values = []

    # Usar select_related para otimizar consultas
    if nome or status:
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

            # Filtra colaboradores com base no nome
            values_colaboradores = Colaborador.objects.filter(
                nome__icontains=nome
            )
        if status:
            # Filtra empréstimos com base no status
            values = Emprestimo.objects.select_related('colaborador', 'equipamento').filter(
                status=status
            )
    else:
        values = Emprestimo.objects.select_related('colaborador', 'equipamento').all()
        values_equipamentos = Equipamento.objects.all()
        values_colaboradores = Colaborador.objects.all()

    # Processa os empréstimos filtrados
    emprestimos = []
    for value in values:
        emprestimo = {
            'id': value.id,
            'data_emprestimo': value.data_emprestimo,
            'data_prevista_devolucao': value.data_prevista_devolucao,
            'data_devolucao': value.data_devolucao,
            'colaborador': value.colaborador.nome,  # Objeto completo já obtido por select_related
            'equipamento': value.equipamento.nome,  # Objeto completo já obtido por select_related
            'quantidade_equipamento': value.quantidade_equipamento,
            'observacao': value.observacao,
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

    colaboradores = []
    for value in values_colaboradores:
        colaborador = {
            'id': value.id,
            'nome': value.nome,
            'email': value.email,
        }
        colaboradores.append(colaborador)
    
    context = {
        'lista_emprestimo': emprestimos,
        'lista_equipamentos': equipamentos,
        'lista_colaboradores': colaboradores,
    }
    return render(request, 'myapp/pages/listar.html', context)

@login_required(login_url='/login/login/')
@permission_required('myapp.criar_colaboradores',login_url='/login/login/', raise_exception=True)
def criar_colaborador(request):
    erro = []  # Lista para armazenar mensagens de erro
    nome = None

    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        
        # Verifica se todos os campos foram preenchidos
        if not nome or not data_nascimento or not email:
            erro.append('Todos os campos são obrigatórios!')
        else:
            # Cria o colaborador
            Colaborador.objects.create(nome=nome, data_nascimento=data_nascimento, email=email)
            messages.success(request, 'Colaborador cadastrado com sucesso!', extra_tags='colaborador')
            return render(request, 'myapp/pages/cadastrar_colaborador.html', {"ultimo_nome": nome})  # Redireciona para a lista de colaboradores

        # Se houver erros, renderiza a página novamente com as mensagens
        for msg in erro:
            messages.error(request, msg, extra_tags='colaborador')

        return render(request, 'myapp/pages/cadastrar_colaborador.html', {
            "ultimo_nome": nome,
        })
    
    return render(request, 'myapp/pages/cadastrar_colaborador.html', {"ultimo_nome": nome})


@login_required(login_url='/login/login/')
@permission_required('myapp.atualizar_colaborador',login_url='/login/login/', raise_exception=True)
def atualizar_colaborador(request, id):
    item = Colaborador.objects.get(id=id)
    if request.method == 'POST':
        itemNome = request.POST.get('nome')
        itemDataNascimento = request.POST.get('data_nascimento')  # Captura a data de nascimento
        itemEmail = request.POST.get('email')
        
        if itemNome and itemDataNascimento and itemEmail:
            # Cria o colaborador com a data de nascimento
            item.nome = itemNome
            item.data_nascimento = itemDataNascimento
            item.email = itemEmail
            item.save()
            return redirect(listar_emprestimo)
    return render(request, 'myapp/pages/atualizar_colaborador.html', {"item": item})

@login_required(login_url='/login/login/')
@permission_required('myapp.deletar_colaborador',login_url='/login/login/', raise_exception=True)
def deletar_colaborador(request, id):
    item = Colaborador.objects.get(id=id)
    item.delete()
    return redirect(listar_emprestimo)

@login_required(login_url='/login/login/')
@permission_required('myapp.criar_equipamentos',login_url='/login/login/', raise_exception=True)
def criar_equipamento(request):
    erro = []  # Lista para armazenar mensagens de erro
    nome = None

    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        quantidade = request.POST.get('quantidade')
        
        # Verifica se todos os campos foram preenchidos
        if not nome or not tipo or not quantidade:
            erro.append('Todos os campos são obrigatórios!')
        else:
            # Verifica se já existe um equipamento com o mesmo nome e tipo
            if Equipamento.objects.filter(nome=nome, tipo=tipo).exists():
                erro.append('Equipamento já cadastrado com este nome e tipo!')
            else:
                # Cria o equipamento se não houver duplicidade
                Equipamento.objects.create(nome=nome, tipo=tipo, quantidade=quantidade)
                messages.success(request, 'Equipamento cadastrado com sucesso!', extra_tags='equipamento')
                return render(request, 'myapp/pages/cadastrar_equipamento.html', {"ultimo_nome": nome})  # Redireciona para a lista de equipamentos

        # Se houver erros, renderiza a página novamente com as mensagens
        for msg in erro:
            messages.error(request, msg, extra_tags='equipamento')

        return render(request, 'myapp/pages/cadastrar_equipamento.html', {
            "ultimo_nome": nome,
        })
    
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
                    "erro": "A quantidade deve ser um número válido.",
                    "itemTipo": itemTipo,
                    "itemQuantidade": itemQuantidade_str  # Retorna o valor de quantidade inserido pelo usuário
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
                "erro": "Por favor, preencha todos os campos.",
                "itemTipo": itemTipo,
                "itemQuantidade": itemQuantidade_str  # Retorna o valor de quantidade inserido pelo usuário
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
        return render(request, 'myapp/pages/cadastrar_emprestimo.html', {
            "colaboradores": colaboradores,
            "equipamentos": equipamentos
        })

    elif request.method == 'POST':
        data_emprestimo = request.POST.get('data_emprestimo')
        data_prevista_devolucao = request.POST.get('data_prevista_devolucao')
        colaborador = request.POST.get('colaborador')
        equipamento = request.POST.get('equipamento')
        quantidade_equipamento_str = request.POST.get('quantidade_equipamento')
        status_str = request.POST.get('status')

        erro = []

        if not quantidade_equipamento_str:
            erro.append("Por favor, forneça a quantidade de equipamentos.")
        else:
            try:
                quantidade_equipamento = int(quantidade_equipamento_str)
            except ValueError:
                erro.append("Quantidade deve ser um número válido.")
                quantidade_equipamento = 0

        if data_emprestimo and data_prevista_devolucao and data_emprestimo >= data_prevista_devolucao:
            erro.append("A data prevista de devolução não pode ser anterior à data de empréstimo.")

        try:
            equipamento_id = int(equipamento)
            equipamento_obj = Equipamento.objects.get(id=equipamento_id)
            qnt_equipamento_db = equipamento_obj.quantidade
        except (ValueError, Equipamento.DoesNotExist):
            erro.append("Equipamento não encontrado.")

        if 'qnt_equipamento_db' in locals() and quantidade_equipamento > qnt_equipamento_db:
            erro.append("Quantidade de equipamentos insuficiente.")

        if erro:
            for msg in erro:
                messages.error(request, msg, extra_tags='emprestimo')
            colaboradores = Colaborador.objects.all()
            equipamentos = Equipamento.objects.all()
            return render(request, 'myapp/pages/cadastrar_emprestimo.html', {
                "colaboradores": colaboradores,
                "equipamentos": equipamentos
            })

        status = status_str == "Emprestado"

        emprestimo = Emprestimo.objects.create(
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao,
            colaborador_id=colaborador,
            equipamento_id=equipamento_id,
            status=status,
            quantidade_equipamento=quantidade_equipamento
        )

        if status:
            equipamento_obj.quantidade -= quantidade_equipamento
        else:
            equipamento_obj.quantidade += quantidade_equipamento
        
        equipamento_obj.save()

        messages.success(request, 'Empréstimo registrado com sucesso!', extra_tags='emprestimo')

        return render(request, 'myapp/pages/cadastrar_emprestimo.html', {"colaboradores": colaboradores, "equipamentos": equipamentos})

    return render(request, 'myapp/pages/cadastrar_emprestimo.html', {"colaboradores": colaboradores, "equipamentos": equipamentos})



@login_required(login_url='/login/login/')
@permission_required('myapp.atualizar_emprestimos',login_url='/login/login/', raise_exception=True)
def atualizar_emprestimo(request, id):
    emprestimo = Emprestimo.objects.get(id=id)
    equipamento = emprestimo.equipamento  # Obtém o equipamento associado ao empréstimo

    if request.method == 'POST':
        status = request.POST.get('status')
        data_devolucao = request.POST.get('data_devolucao')
        observacao = request.POST.get('observacao')

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not status:
            erro = "Por favor, selecione um status."
        elif status in ['Devolvido', 'Danificado', 'Perdido'] and (not data_devolucao or not observacao):
            erro = "Por favor, preencha a data de devolução e/ou observação."
        else:
            erro = None

        # Se houver erro, reexibe o formulário com a mensagem de erro
        if erro:
            return render(request, 'myapp/pages/atualizar_emprestimo.html', {"item": emprestimo, "erro": erro})

        try:
            # Ajusta a quantidade de equipamentos com base no status anterior e no novo status
            if emprestimo.status:  # Status atual é 'Emprestado'
                if status == 'Devolvido' or status == 'Danificado' or status == 'Perdido':
                    # Se está mudando para 'Devolvido', 'Danificado' ou 'Perdido', aumenta a quantidade
                    equipamento.quantidade += emprestimo.quantidade_equipamento
            else:  # Status atual é 'Devolvido', 'Danificado' ou 'Perdido'
                if status == 'Emprestado':
                    if equipamento.quantidade >= emprestimo.quantidade_equipamento:
                        equipamento.quantidade -= emprestimo.quantidade_equipamento
                    else:
                        erro = "Não há quantidade suficiente de equipamentos para emprestar."
                        return render(request, 'myapp/pages/atualizar_emprestimo.html', {"item": emprestimo, "erro": erro})

            # Atualiza o status do empréstimo
            emprestimo.status = (status == 'Emprestado')  # Converte o status para booleano

            if status in ['Devolvido', 'Danificado', 'Perdido']:
                emprestimo.data_devolucao = data_devolucao
                emprestimo.observacao = observacao

            emprestimo.save()
            equipamento.save()

            return redirect('listar_emprestimo')  # Redireciona para a lista de empréstimos

        except Exception as e:
            erro = f'Ocorreu um erro ao atualizar o empréstimo: {e}'
            return render(request, 'myapp/pages/atualizar_emprestimo.html', {"item": emprestimo, "erro": erro})

    return render(request, 'myapp/pages/atualizar_emprestimo.html', {"item": emprestimo})

@login_required(login_url='/login/login/')
@permission_required('myapp.atualizar_emprestimos',login_url='/login/login/', raise_exception=True)
def deletar_emprestimo(request, id):
    emprestimo = Emprestimo.objects.get(id=id)
    emprestimo.delete()
    return redirect('listar_emprestimo')


def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    nome = request.GET.get('nome')
    if nome:
        colaboradores = colaboradores.filter(nome__icontains=nome)

    return render(request, 'myapp/pages/listar.html', {"colaboradores": colaboradores})


def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    nome = request.GET.get('nome')
    if nome:
        equipamentos = equipamentos.filter(nome__icontains=nome)

    return render(request, 'myapp/pages/listar.html', {"equipamentos": equipamentos})
