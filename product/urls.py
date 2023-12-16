from django.urls import path

from product.apps import ProductConfig
from product.views import *

app_name = ProductConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view'),
    path('contacts/', contacts, name='contacts'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete')
]
