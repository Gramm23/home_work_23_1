from django.urls import path

from materials.views import *

app_name = 'materials'

urlpatterns = [
    path('', MaterialsListView.as_view(), name='material_list'),
    path('create/', MaterialsCreateView.as_view(), name='material_create'),
    path('view/<int:pk>/', MaterialsDetailView.as_view(), name='material_detail'),
    path('edit/<int:pk>/', MaterialsUpdateView.as_view(), name='material_edit'),
    path('delete/<int:pk>/', MaterialsDeleteView.as_view(), name='material_delete')
]

