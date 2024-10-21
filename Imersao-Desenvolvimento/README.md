
# Projeto de U.C. Desenvolvimento de Sistema

Este projeto tem como objetivo desenvolver uma aplicação web utilizando Django para gerenciar o empréstimo de Equipamentos de Proteção Individual (EPIs). A aplicação permitirá que usuários e colaboradores realizem empréstimos de equipamentos de forma simples e intuitiva. Além disso, administradores ou supervisores terão acesso a funcionalidades para cadastrar, atualizar e gerenciar os equipamentos disponíveis.

## Funcionalidades

- **Cadastrar Colaborador**: Permite que supervisores registrem os colaboradores a acesserem o sistema.
- **Fazer Empréstimo**: Usuários podem solicitar o empréstimo de EPIs disponíveis.
- **Gerenciamento de Equipamentos**: Administradores podem adicionar, editar e remover equipamentos da lista.
- **Histórico de Empréstimos**: Visualização de todos os empréstimos realizados, com detalhes sobre o usuário, equipamento e data.


## Tecnologias Utilizadas

- **Django**: Framework web para desenvolvimento rápido e eficiente.
- **SQLite**: Banco de dados leve para armazenar informações de usuários e equipamentos.
- **HTML/CSS**: Para estruturação e estilização das páginas web.

## Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/lArauj0/Imersao-Desenvolvimento.git
   cd repo

2. Usando Docker:
   ```bash
   docker-compose up --build

3. Interagir com o Container:
   ```bash
   docker exec -it senai_desi bash

3. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   venv\Scripts\activate

4. Instale as Dependências:
   ```bash
   pip install -r requirements.txt

6. Paassar o Banco de Dados:
   ```bash
   python manage.py migrate

8. Execute o Servidor de Desenvolvimento:
    ```bash
    python manage.py runserver

9. Acesse a Aplicação digitando:
   ```bash
   http://127.0.0.1:8000

11. Parar e Remover os Containers:
      ```bash
      docker-compose down

10. Desative o Ambiente Virtual:
   ```bash
   deactivate

