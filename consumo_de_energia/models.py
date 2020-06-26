from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import signals
from Consumo2.utils import slug_pre_save

# Create your models here.

class AparelhoManager(models.Manager):
    
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(potencia__icontains=query))

class Aparelho(models.Model):

    STATUS_CHOICES = (
        (1, 'minutos/dia'),
        (2, 'horas/dia'),
    )
    
    name = models.CharField(verbose_name='Nome do aparelho', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Atalho', default='', editable=False, max_length=100)
    quantidade = models.IntegerField('Quantidade', default=1, blank=True)
    potencia = models.IntegerField(verbose_name='Potencia em watts', null=True, blank=True)
    tempo = models.IntegerField(verbose_name='Tempo de uso',null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=2, blank=True, verbose_name='')
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)


    objects = AparelhoManager()

    def __str__(self):
        return self.name
        
    @property
    def calculoKw(self):
        pot = 0
        time = 0
        consumo = 0
        if self.status == 1:
            pot = (self.quantidade * self.potencia) / 1000
            time = self.tempo / 60
            consumo = pot * time
            print(consumo)
            return f'{consumo:.2f}'.replace('.',',')
        else:
            pot = (self.quantidade * self.potencia) / 1000
            consumo = pot * self.tempo
            print(consumo)
            return f'{consumo:.2f}'.replace('.',',')
    
    
    def tarifa(self):
        pot = 0
        time = 0
        consumo = 0
        if self.status == 1:
            pot = (self.quantidade * self.potencia) / 1000
            time = self.tempo / 60
            consumo = pot * time * 0.733363
            print(consumo)
            return f'{consumo:.2f}'.replace('.',',')
        else:
            pot = (self.quantidade * self.potencia) / 1000
            consumo = pot * self.tempo * 0.733363

            print(consumo)
            return f'{consumo:.2f}'.replace('.',',')

    def get_absolute_url(self):
        return reverse('consumo:detail_app', kwargs={'slug' : self.slug})
    '''
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True).replace("'","")
        super().save(*args, **kwargs)
    '''

    class Meta:
        db_table = 'aparelho'
        verbose_name = 'aparelho'
        verbose_name_plural = 'Aparelho'
        ordering = ['name']
    

class Ambiente(models.Model):

    name = models.CharField(verbose_name='Nome do ambiente', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Atalho', default='', editable=False, max_length=100)
    created_at = models.DateTimeField(verbose_name='Criado em',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)
    aparelhos = models.ManyToManyField(Aparelho, 
        related_name='aparelhos_no_ambiente', 
        db_table='aparelho_ambiente', blank=True,
        verbose_name='Selecione os aparelhos'
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('consumo:ambientes_apps_list', kwargs={'slug' : self.slug})
    
    '''
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    '''
    
    class Meta:
        db_table = 'ambiente'
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'
        ordering = ['name']


signals.pre_save.connect(slug_pre_save, sender=Aparelho)
signals.pre_save.connect(slug_pre_save, sender=Ambiente)
