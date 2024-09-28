from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.



class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True)  # Novo campo
    email = models.EmailField()

    @property
    def idade(self):
        return date.today().year - self.data_nascimento.year - (
            (date.today().month, date.today().day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    
    
class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    quantidade = models.IntegerField()

class Emprestimo(models.Model):
    data_emprestimo = models.DateField()
    data_devolucao = models.DateField()
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    quantidade_equipamento = models.IntegerField(null=True)
    status = models.BooleanField()

    def clean(self):
        if self.data_devolucao < self.data_emprestimo:
            raise ValidationError('A data de devolução não pode ser anterior à data de empréstimo.')

    def __str__(self):
        return f'Colaborador:{self.colaborador}, Equipamento:{self.equipamento}, Status:{self.status}'