from django import forms
from .models import Aparelho, Ambiente
from bootstrap_modal_forms.forms import BSModalForm

#criação do formulario de preenchimento do aparelho.

class AparelhoForm(forms.ModelForm):

    class Meta:
        model = Aparelho
        fields = ['name','quantidade','potencia', 'tempo', 'status']

class AppForm(BSModalForm):

    class Meta:
        model = Aparelho
        fields = ['name','quantidade','potencia', 'tempo', 'status']

class AmbienteForm(forms.ModelForm):

    class Meta:
        model = Ambiente
        fields = ['name']

class InsertAppForm(forms.ModelForm):
    name = forms.CharField(disabled=True)
    class Meta:
        model = Ambiente
        fields = ['name', 'aparelhos']