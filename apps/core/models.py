from django.db import models


class DefaultModel(models.Model):
    created_at = models.DateTimeField('Criado em', auto_now=True)
    updated_at = models.DateTimeField('Atualizado em'auto_now_add=True)

    class Meta:
        abstract = True
