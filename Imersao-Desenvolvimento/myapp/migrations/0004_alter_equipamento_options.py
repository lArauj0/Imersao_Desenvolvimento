# Generated by Django 5.1 on 2024-10-10 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_colaborador_idade_colaborador_data_nascimento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipamento',
            options={'permissions': [('deletar_equipamentos', 'Pode deletar equipamentos'), ('editar_equipamentos', 'Pode editar equipamentos')]},
        ),
    ]