from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from myapp.views import listar_emprestimo
from django.contrib.auth.models import Group, Permission

# login_app/views.py
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.storage import FileSystemStorage

def criar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')  # Verifica o arquivo

        if all([nome, sobrenome, email, username, password]):
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=nome,
                last_name=sobrenome 
            )
            profile = Profile(user=user, profile_image=profile_image)
            profile.save()

            messages.success(request, 'Usuário criado com sucesso!')
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios.')

        return redirect('login_usuario')
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
