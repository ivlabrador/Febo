from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from .models import Provider
from .forms import ProviderForm
from django.urls import reverse_lazy
from config.permission import ValidatePermission
from django.contrib import messages
# Create your views here.
class AddProvider(ValidatePermission, CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'add_provider.html'
    success_url = reverse_lazy('list-provider')
    url_redirect = success_url
    permission_required = 'change_provider'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                else:
                    # Mensaje de error
                    data['error'] = form.errors
            else:
                #Mensaje de error
                return redirect('add-provider')

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# List Provider
class ListProvider(ValidatePermission, ListView):
    model = Provider
    template_name = 'list_provider.html'
    permission_required = 'view_provider'
    url_redirect = reverse_lazy('list-provider')
    create_url = reverse_lazy('add-provider')

    data = {}
    try:
        providers = Provider.objects.all()
    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de proveedores'
        context['entity'] = 'Proveedores'
        context['providers'] = Provider.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Product
class UpdateProvider(ValidatePermission, UpdateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'add_provider.html'
    success_url = reverse_lazy('list-provider')
    url_redirect = success_url
    permission_required = 'change_provider'

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
                return redirect(self.success_url)
            else:
                messages.warning(request, f'Error al editar el proveedor')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Delete Provider
class DeleteProvider(DeleteView, ValidatePermission):
    model = Provider
    success_url = reverse_lazy('list-provider')
    url_redirect = success_url
    permission_required = 'delete_provider'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                provider_id = request.POST['provider_id']
                provider = Provider.objects.get(pk=provider_id)
                provider.delete()
                messages.success(request, f'Producto eliminado: {provider.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el proveedor')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url

        return context