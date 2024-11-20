from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from myapp.views import listar_emprestimo
from django.contrib.auth.models import Group, Permission

# login_app/views.py
from django.contrib import messages

def criar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        foto_url = request.POST.get('foto_url')  # Pega a URL da foto

        # Criar o usuário
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = nome
            user.last_name = sobrenome
            user.profile.foto_url = foto_url  # Salvar a URL da foto no campo do perfil
            user.save()

            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar_emprestimo')  # Redireciona para a página inicial ou outra página após o cadastro
        except Exception as e:
            messages.error(request, 'Erro ao cadastrar o usuário: {}'.format(e))

    print("Acessou a view criar_usuario")
    return render(request, 'login_app/pages/cadastrar.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(listar_emprestimo)
            mensagem = 'Usuário ou senha inválidos'
            return render(request, 'login_app/pages/login.html', {'erro': mensagem})
    return render(request, 'login_app/pages/login.html')


def logout_usuario(request):
    logout(request)
    return redirect(login_usuario)
