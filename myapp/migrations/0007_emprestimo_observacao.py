# Generated by Django 5.1 on 2024-11-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_emprestimo_data_prevista_devolucao'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='observacao',
            field=models.TextField(null=True),
        ),
    ]
