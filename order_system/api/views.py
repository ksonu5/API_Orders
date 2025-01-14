from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer
import csv
from django.http import HttpResponse
from .models import Order, Item

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


def download_orders_csv(request):
    # Create an HTTP response with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders_summary.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['Order ID', 'Item ID', 'Item Name', 'Quantity', 'Date'])

    # Fetch data from the Order model
    orders = Order.objects.select_related('item_id')  # Optimized for related fields
    for order in orders:
          writer.writerow([
            order.id,
            order.item_id.id,       # Use correct field name
            order.item_id.name,     # Access related Item's name
            order.quantity,
            order.created_at,
        ])
          
    if not orders.exists():
         writer.writerow(['No data available'])

    return response
