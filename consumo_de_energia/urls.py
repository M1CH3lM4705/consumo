from django.urls import path
from consumo_de_energia import views

app_name = 'consumo'

urlpatterns = [
    path('ambientes/',views.list_ambiente, name='list_ambiente'),
    path('aparelhos/',views.list_aparelho, name='list_aparelho'),
    path('ambiente/<slug:slug>/',views.list_ambiente_aparelho, name='ambientes_apps_list'),
    path('aparelho/details/<slug:slug>/',views.AppReadView.as_view(), name='details_app'),
    path('aparelho/detail/<slug:slug>/',views.details_app, name='detail_app'),
    path('ambiente/<slug:slug>/inserir-aparelhos/', views.insert_app_amb ,name='ambientes_apps_insert'), 
    path('add/aparelho/', views.save_aparelho, name='add_aparelho'),
    path('add/aparelho/model/', views.AppModalCreate.as_view(), name='add_app_modal'), 
    path('delete/aparelho/model/<int:pk>/<slug:slug>/', views.delete_app_ambiente, name='del_app_modal'),
    path('add/ambiente/', views.save_ambiente, name='add_ambiente'),
    path('edit/ambiente/<slug:slug>/', views.edit_ambiente, name='edit_ambiente'), 
    path('edit/aparelho/<slug:slug>/', views.edit_aparelho, name='edit_aparelho'), 
    path('edit/aparelho/modal/<slug:slug>/', views.edit_modal_aparelho, name='edit_modal_aparelho'),
    path('ambientes/delete/<slug:slug>/', views.delete_ambiente, name='delete_ambiente'),
    path('aparelhos/delete/<slug:slug>/', views.delete_aparelho, name='delete_aparelho'),
]