import json
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from .forms import LotForm
from .models import Lot, Stock, LotProduct
from config.permission import ValidatePermission
from .utilities import calculate_stock, is_boolean
from django.contrib import messages
# Categories
from ..product.models import Product
from ..provider.forms import ProviderForm
from ..provider.models import Provider
from ..purchase.models import Purchase
from ..user.models import User

# Add Lot
class AddLot(ValidatePermission, CreateView):
    model = Lot
    form_class = LotForm
    template_name = 'add_lot.html'
    success_url = reverse_lazy('list-stock')
    url_redirect = success_url
    form_error_url = reverse_lazy('add-lot')
    url_render_error = form_error_url
    permission_required = 'add_lot'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        id_session = request.user.id
        action = request.POST['action']
        if action == 'search_products':
            data = []
            ids_exclude = json.loads(request.POST['ids'])
            term = request.POST['term'].strip()
            data.append({'id': term, 'text': term})
            products = Product.objects.filter(name__icontains=term).filter(Q(is_active=True))
            for i in products.exclude(id__in=ids_exclude)[0:10]:
                item = i.toJSON()
                item['text'] = i.__str__()
                data.append(item)
        elif action == 'add':
            with transaction.atomic():
                subtotal = float(request.POST['subtotal'])
                total_discount = float(request.POST['total_discount'])
                total_iva = float(request.POST['total_iva'])
                total = subtotal + total_iva - total_discount
                provider = Provider.objects.get(pk=int(request.POST['provider']))
                user = User.objects.get(pk=id_session)
                make_invoice = request.POST.get('make_invoice', 'off')
                make_invoice = is_boolean(make_invoice)
                is_pay = request.POST.get('is_pay', 'off')
                is_pay = is_boolean(is_pay)
                pdf_file = request.POST.get('payment_slip', None)
                lot = Lot(
                    provider=provider,
                    lot_date=request.POST['lot_date'],
                    buy_num=request.POST['buy_num'],
                    buy_type=request.POST['buy_type'],
                    pay_condition=request.POST['pay_condition'],
                    pay_type=request.POST['pay_type'],
                    subtotal=subtotal,
                    total_iva=total_iva,
                    total_discount=total_discount,
                    total=total,
                    payment_slip=pdf_file,
                    make_invoice=make_invoice,
                    is_pay=is_pay,
                    charger=user
                )
                lot.save()
                lot_number = str(lot.id)
                products = json.loads(request.POST['products'])
                for i in products:
                    detail = LotProduct()
                    detail.lot_id = lot.pk
                    detail.product_id = int(i['id'])
                    detail.quantity = int(i['quantity'])
                    detail.price = float(i['price'])
                    detail.discount = float(i['discount'])
                    detail.subtotal = (detail.quantity * detail.price)
                    detail.save()
                    # Comprobacíon de que el producto se encuentre o no en Stock
                    try:
                        stock = Stock.objects.get(product_id=i['id'])
                        stock.stock += int(i['quantity'])
                        stock.lots.append(lot_number)
                        stock.save()
                    except ObjectDoesNotExist:
                        stock = Stock(
                            product_id=int(i['id']),
                            lots=lot_number,
                            stock=int(i['quantity']),
                        )
                        stock.save()
                    except Exception as e:
                        messages.error(request, f'Error: {e}')
                        return redirect('add-lot')
                messages.success(request, 'Lote cargado con éxito')
        elif action == 'search_provider':
                data = []
                term = request.POST['term']
                providers = Provider.objects.filter(Q(name__icontains=term) | Q(f_name__icontains=term))[0:10]
                for i in providers:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
        else:
            data['error'] = 'No ha ingresado a ninguna opción'

        return JsonResponse(data, safe=False)
   
        # Buscar Proveedor



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar lote'
        context['entity'] = 'Lotes'
        context['list_url'] = self.url_redirect
        context['action'] = 'add'
        context['products'] = []
        context['add-provider-form'] = ProviderForm
        return context

# List Lot
class ListLot(ValidatePermission, ListView):
    model = Lot
    template_name = 'list_lot.html'
    permission_required = 'view_lot'
    url_redirect = reverse_lazy('list-lot')
    create_url = reverse_lazy('add-lot')

    data = {}
    try:
        lots = Lot.objects.all()

    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de lotes'
        context['entity'] = 'Lotes'
        context['lots'] = Lot.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Lot
class UpdateLot(ValidatePermission, UpdateView):
    model = Lot
    form_class = LotForm
    template_name = 'add_lot.html'
    success_url = reverse_lazy('list-lot')
    url_redirect = success_url
    permission_required = 'change_lot'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            obj = self.get_object()
            id = obj.id
            if form.is_valid():
                lot = Lot.objects.get(pk=id)
                instance = LotForm(request.POST or None, request.FILES or None, instance=lot)
                product = request.POST['product']
                instance.save()
                messages.success(request, f'Lote editado con éxito, producto: {product}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, 'Hay errores en el formulario de edición')
                return redirect(self.url_redirect)

# Delete Provider
class DeleteLot(DeleteView, ValidatePermission):
    model = Lot
    success_url = reverse_lazy('list-lot')
    url_redirect = success_url
    permission_required = 'delete_lot'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                lot_id = request.POST['lot_id']
                lot = Lot.objects.get(pk=lot_id)
                # Eliminar Factura si es que existe y crea factura nueva
                if lot.make_invoice:
                    purchase = Purchase.objects.filter(provider=lot.provider, buy_num=lot.buy_num, total=lot.total).get()
                    purchase.delete()
                else:
                    pass
                lot_products = LotProduct.objects.filter(lot_id=lot_id).all()
                for product in lot_products:
                    stock = Stock.objects.get(product_id=product.product.id)
                    stock.stock -= int(product.quantity)
                    stock.lots.remove(str(lot_id))
                    stock.save()
                    product.delete()
                lot.delete()
                messages.success(request, f'Lot N°: {lot_id}, eliminado con éxito')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el lote')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar lot'
        context['entity'] = 'Stock'
        context['list_url'] = self.success_url

        return context


# List Stock
class ListStock(ValidatePermission, ListView):
    model = Lot
    template_name = 'list_stock.html'
    permission_required = 'view_stock'
    url_redirect = reverse_lazy('list-stock')
    create_url = reverse_lazy('add-lot')

    data = {}
    try:
        stocks = Stock.objects.all()

    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de stock'
        context['entity'] = 'Stock'
        context['stocks'] = Stock.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context