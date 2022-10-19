import json
from django.db.models import Q, FloatField
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, View, ListView, TemplateView
from config.permission import ExistsCompany, ValidatePermission
from core.client.forms import ClientForm
from .models import Sale, SalePoint
from .models import SaleProduct
from .forms import SaleForm, SalePointForm, ReportSaleForm
from core.product.models import Product
from core.client.models import Client
from core.stock.models import Stock
from core.stock.utilities import is_boolean
from ..user.models import User
from django.contrib import messages
# PDF
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
#Report
from django.db.models import Sum
from django.db.models.functions import Coalesce

# Add Sale Point
class AddSalePoint(ValidatePermission, CreateView):
    model = SalePoint
    form_class = SalePointForm
    template_name = 'add_sale_point.html'
    success_url = reverse_lazy('list-sale')
    url_redirect = success_url
    permission_required = 'add_sale_point'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                else:
                    data['error'] = form.errors
            else:
                return redirect('add-sale-point')

        except Exception as e:
            data['error'] = str(e)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Punto de Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# Add Sale
class AddSale(ValidatePermission, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'add_sale.html'
    success_url = reverse_lazy('list-sale')
    url_redirect = success_url
    permission_required = 'add_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        id_session = int(request.user.id)
        if action == 'search_products':
            data = []
            ids_exclude = json.loads(request.POST['ids'])
            term = request.POST['term'].strip()
            data.append({'id': term, 'text': term})
            products = Product.objects.filter(name__icontains=term).filter(Q(is_active=True))
            for i in products.exclude(id__in=ids_exclude)[0:10]:
                product_in_stock = Stock.objects.get(product_id=i.pk)
                stock = int(product_in_stock.stock)
                item = i.toJSON()
                item['text'] = i.__str__()
                item['stock'] = stock
                data.append(item)
        elif action == 'add':
            with transaction.atomic():
                products = json.loads(request.POST['products'])
                subtotal = float(request.POST['subtotal'])
                total_discount = float(request.POST['total_discount'])
                total_iva = float(request.POST['total_iva'])
                total = (subtotal + total_iva - total_discount)
                is_pay = request.POST.get('is_pay', 'off')
                is_pay = is_boolean(is_pay)
                sale = Sale(
                    date_sale=request.POST['date_sale'],
                    client_id=int(request.POST['client']),
                    sale_point_id=int(request.POST['sale_point']),
                    sale_num=request.POST['sale_num'],
                    sale_type=request.POST['sale_type'],
                    pay_condition=request.POST['pay_condition'],
                    pay_type=request.POST['pay_type'],
                    total_discount=total_discount,
                    total_iva=total_iva,
                    subtotal=subtotal,
                    total=total,
                    charger_id=id_session,
                    is_pay=is_pay,
                )
                sale.save()
                for i in products:
                    detail = SaleProduct()
                    detail.sale_id = sale.id
                    detail.product_id = int(i['id'])
                    detail.quantity = int(i['quantity'])
                    detail.price = float(i['price'])
                    detail.discount = float(i['discount'])
                    detail.subtotal = detail.quantity * detail.price
                    detail.save()
                    if detail.product.is_active:
                        detail.stock.stock -= detail.quantity
                        detail.stock.quantity_sold += detail.quantity
                        detail.stock.save()
                #sale.calculate_invoice()
                data = {'id': sale.id}
        elif action == 'search_client':
            data = []
            term = request.POST['term']
            clients = Client.objects.filter(Q(name__icontains=term) | Q(f_name__icontains=term))[0:10]
            for i in clients:
                item = i.toJSON()
                item['text'] = i.__str__()
                data.append(item)
        else:
            data['error'] = 'No ha ingresado a ninguna opción'

        return JsonResponse(data, safe=False) #Safe = False para serializarlo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        context['add-client-form'] = ClientForm
        return context

# List Sale
class ListSale(ValidatePermission, ListView):
    model = Sale
    template_name = 'list_sale.html'
    permission_required = 'view_sale'
    url_redirect = reverse_lazy('list-sale')
    create_url = reverse_lazy('add-sale')

    data = {}
    try:
        categories = Sale.objects.all()
    except Exception as e:
        data['error'] = str(e)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de ventas'
        context['entity'] = 'Ventas'
        context['sales'] = Sale.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Sale
class UpdateSale(ValidatePermission, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'add_sale.html'
    success_url = reverse_lazy('list-sale')
    url_redirect = success_url
    permission_required = 'change_sale'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
        return form

    def get_details_product(self):
        data = []
        sale = self.get_object()
        for i in sale.saleproduct_set.all():
            stock = i.stock.stock
            stock += int(i.quantity)
            item = i.product.toJSON()
            item['quantity'] = i.quantity
            item['price'] = str(i.price)
            item['discount'] = str(i.discount)
            item['stock'] = str(stock)
            data.append(item)
        return json.dumps(data)

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
                product_in_stock = Stock.objects.get(product_id=i.pk)
                stock = int(product_in_stock.stock)
                item = i.toJSON()
                item['text'] = i.__str__()
                item['stock'] = stock
                data.append(item)
        elif action == 'edit':
            products = json.loads(request.POST['products'])
            sale = self.get_object()
            subtotal = float(request.POST['subtotal'])
            total_discount = float(request.POST['total_discount'])
            total_iva = float(request.POST['total_iva'])
            total = (subtotal + total_iva - total_discount)
            is_pay = request.POST.get('is_pay', 'off')
            is_pay = is_boolean(is_pay)
            sale.date_sale = request.POST['date_sale']
            sale.client_id = int(request.POST['client'])
            sale.sale_point_id = int(request.POST['sale_point'])
            sale.sale_num = request.POST['sale_num']
            sale.sale_type = request.POST['sale_type']
            sale.pay_condition = request.POST['pay_condition']
            sale.pay_type = request.POST['pay_type']
            sale.subtotal = subtotal
            sale.total_iva = total_iva
            sale.total_discount = total_discount
            sale.total = total
            sale.is_pay = is_pay
            sale.charger_id = id_session
            sale.save()
            # Cargar el stock verdadero  y guardarlo
            for detail in sale.saleproduct_set.all():
                stock = Stock.objects.get(product_id=detail.product.id)
                stock.stock += int(detail.quantity)
                stock.save()
            sale.saleproduct_set.all().delete()
            # Instanciar nuevamente todos los detalles
            for i in products:
                detail = SaleProduct()
                detail.sale_id = sale.id
                detail.product_id = int(i['id'])
                detail.quantity = int(i['quantity'])
                detail.price = float(i['price'])
                detail.subtotal = detail.quantity * detail.price
                detail.save()
                if detail.product.is_active:
                    detail.stock.stock -= detail.quantity
                    detail.stock.quantity_sold += detail.quantity
                    detail.stock.save()
            # sale.calculate_invoice()
            data = {'id': sale.id}
        elif action == 'search_client':
            data = []
            term = request.POST['term']
            clients = Client.objects.filter(Q(name__icontains=term) | Q(f_name__icontains=term))[0:10]
            for i in clients:
                item = i.toJSON()
                item['text'] = i.__str__()
                data.append(item)
        else:
            data['error'] = 'No ha ingresado a ninguna opción'

        return JsonResponse(data, safe=False)  # Safe = False para serializarlo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['add-client-form'] = ClientForm
        return context

# Delete Sale
class DeleteSale(ValidatePermission, DeleteView):
    model = Sale
    success_url = reverse_lazy('list-sale')
    url_redirect = success_url
    permission_required = 'delete_sale'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                sale_id = request.POST['sale_id']
                sale = Sale.objects.get(pk=sale_id)
                sale_num = sale.sale_num
                sale_point = sale.sale_point.number
                client = sale.client
                sale_products = SaleProduct.objects.filter(sale_id=sale_id).all()
                for product in sale_products:
                    quantity = int(product.quantity)
                    stock = Stock.objects.get(product_id=product.product.id)
                    stock.stock += quantity
                    stock.quantity_sold -= quantity
                    stock.save()
                    product.delete()
                sale.delete()
                messages.success(request, f'Venta sobre factura N°:{sale_point}-{sale_num}\nCliente: {client}\nEliminada con éxito')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar la venta, intente nuevamente')
                return redirect(self.success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar una venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context

# MakeInvoice
class MakePDFInvoice(ValidatePermission, View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):

        template = get_template('invoice.html')
        context = {
            'sale': Sale.objects.get(pk=self.kwargs['pk']),
            'icon': f'{settings.MEDIA_URL}febo.png'
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback) #link_callback=link_callback) archivos estaticos

        return response
        #except Exception as e:
         #   print(e)
          #  pass
        #return HttpResponseRedirect(reverse_lazy('list-sale'))

#Make Report
class ReportSale(TemplateView):
    template_name = 'report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search_filter = search.filter(date_sale__range=[start_date, end_date])
                for s in search_filter:
                    data.append([
                        s.sale_num,
                        s.date_sale.strftime('%d-%m-%Y'),
                        s.sale_type,
                        s.client.f_name,
                        format(s.subtotal, '.2f'),
                        format(s.total_iva, '.2f'),
                        format(s.total_discount, '.2f'),
                        format(s.total, '.2f')
                    ])
                # Totales
                subtotal = search_filter.aggregate(r=Coalesce(Sum('subtotal'), 0.0, output_field=FloatField())).get('r')
                total_iva = search_filter.aggregate(r=Coalesce(Sum('total_iva'), 0.0, output_field=FloatField())).get('r')
                total_discount = search_filter.aggregate(r=Coalesce(Sum('total_discount'), 0.0, output_field=FloatField())).get('r')
                total = search_filter.aggregate(r=Coalesce(Sum('total'), 0.0, output_field=FloatField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(total_iva, '.2f'),
                    format(total_discount, '.2f'),
                    format(total, '.2f'),
                ])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report-sale')
        context['form'] = ReportSaleForm()
        return context