# Generated by Django 5.0.4 on 2024-04-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0002_dadosmedico'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosmedico',
            name='status',
            field=models.CharField(choices=[('aprovado', 'Aprovado'), ('negado', 'Negado'), ('analise', 'Análise')], default='analise', max_length=8),
        ),
    ]
