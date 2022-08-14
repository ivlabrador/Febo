
import json
import os

from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy

from django.views.generic import CreateView, FormView, DeleteView, UpdateView, View
from config.permission import ExistsCompany, ValidatePermission
from core.client.forms import ClientForm
from .models import Sale
from .models import SaleProduct
from .forms import SaleForm, ItemForm
from core.product.models import Product
from core.client.models import Client



class AddSale(ExistsCompany, ValidatePermission, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'add_sale.html'
    success_url = reverse_lazy('dashboard')
    url_redirect = success_url
    permission_required = 'add_sale'
    items = []


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.POST:
                with transaction.atomic():
                    print(request.POST)
                    items = json.loads(request.POST['items'])
                    sale = Sale()
                    sale.date_sale = request.POST['date_sale']
                    sale.client_id = int(request.POST['client'])
                    sale.iva = float(request.POST['iva'])
                    sale.save()
                    for i in self.items:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(i['id'])
                        detail.quantity = int(i['cant'])
                        detail.price = float(i['pvp'])
                        detail.subtotal = detail.quantity * detail.price
                        detail.save()
                        if detail.product.is_inventoried:
                            detail.product.stock -= detail.quantity
                            detail.product.save()
                    sale.calculate_invoice()
                    data = {'id': sale.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['items'] = self.items
        context['ItemForm'] = ItemForm
        context['additem'] = self.add_item(self.request)
        return context


    def add_item(self,request, item=None):
        if request.method == 'POST':
            self.items.append(item)
            print(self.items)
            return self.items