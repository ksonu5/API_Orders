from django.urls import path
from . import views

urlpatterns = [
    path('download-orders-csv/', views.download_orders_csv, name='download_orders_csv'),
]
