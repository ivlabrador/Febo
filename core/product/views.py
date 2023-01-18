from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CategoryForm, ProductForm, MassiveProductForm
from .models import Category, Product, MassiveProduct
from config.permission import ValidatePermission
from django.contrib import messages
from config import settings as s
import os
from .massive_tools import make_massive_charge, check_categories, is_active
# Categories

# Create Category
from ..user.models import User


class CreateCategory(ValidatePermission, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('list-category')
    url_redirect = success_url
    create_url = reverse_lazy('add-category')
    permission_required = 'add_category'


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
                return redirect('add-category')

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar una Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# List Category
class ListCategory(ValidatePermission, ListView):
    model = Category
    template_name = 'list_category.html'
    permission_required = 'view_category'
    url_redirect = reverse_lazy('list-category')
    create_url = reverse_lazy('add-category')

    data = {}
    try:
        categories = Category.objects.all()

    except Exception as e:
        data['error'] = str(e)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de categorías'
        context['entity'] = 'Categorías'
        context['categories'] = Category.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Category
class UpdateCategory(ValidatePermission, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('list-category')
    url_redirect = success_url
    permission_required = 'change_category'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                messages.warning(request, f'Error al editar la categoria')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = self.success_url
        return context


# Delete Cateogry
class DeleteCategory(ValidatePermission, DeleteView):
    model = Category
    success_url = reverse_lazy('list-category')
    url_redirect = success_url
    permission_required = 'delete_category'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                category_id = request.POST['category_id']
                category = Category.objects.get(pk=category_id)
                category.delete()
                messages.success(request, f'Producto eliminado: {category.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el producto')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        return context

# Create your views here.
class CreateProduct(ValidatePermission, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('list-product')
    url_redirect = success_url
    permission_required = 'add_product'

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
                return redirect('add-product')

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# List Product
class ListProduct(ValidatePermission, ListView):
    model = Product
    template_name = 'list_product.html'
    permission_required = 'view_product'
    url_redirect = reverse_lazy('list-product')
    create_url = reverse_lazy('add-product')

    data = {}
    try:
        products = Product.objects.all()
    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de productos'
        context['entity'] = 'Productos'
        context['products'] = Product.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Product
class UpdateProduct(ValidatePermission, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('list-product')
    url_redirect = success_url
    permission_required = 'change_product'

    # A traves del dispatch avisamos que existe un objeto recibido por post
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                messages.warning(request, f'Error al editar el producto')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.url_redirect
        context['action'] = 'edit'

        return context

# Delete Product
class DeleteProduct(ValidatePermission, DeleteView):
    model = Product
    success_url = reverse_lazy('list-product')
    url_redirect = success_url
    permission_required = 'delete_product'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                product_id = request.POST['product_id']
                product = Product.objects.get(pk=product_id)
                product.delete()
                messages.success(request, f'Producto eliminado: {product.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el producto')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url

        return context

# Massive Product Charge
class MassiveCharge(CreateView):
    model = MassiveProduct
    form_class = MassiveProductForm
    template_name = 'massive_product.html'
    success_url = reverse_lazy('list-product')
    url_redirect = success_url
    permission_required = 'massive_product'

    def post(self, request, *args, **kwargs):
        data = {}

        if request.method == 'POST':
            id_session = int(request.user.id)
            user = User.objects.get(pk=id_session)
            action = request.POST['action']
            if action == 'add':
                file = request.FILES['file']
                products = make_massive_charge(file)
                category = Category
                for product in products:
                    instance = Product(
                        name=product[0],
                        brand=product[1],
                        model=product[2],
                        iva=product[3],
                        image=product[4],
                        description=product[6],
                        is_active=is_active(product[7])
                    )
                    instance.save()
                    lista = check_categories(product[5], category)
                    for item in lista:
                        instance.category.add(item)
                    instance.save()
                instance_massive = MassiveProduct(
                    charger=user,
                    file=file,
                )
                instance_massive.save()
                return redirect(reverse_lazy('list-product'))
            else:
                data['error'] = 'Form is not valid'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Carga masiva de productos'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
