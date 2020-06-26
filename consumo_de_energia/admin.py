from django.contrib import admin
from .models import Aparelho
from .models import Ambiente

# Register your models here.

class AparelhoAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'potencia', 'tempo', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Aparelho, AparelhoAdmin)


class AmbienteAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Ambiente, AmbienteAdmin)