from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from .models import Client
from .forms import ClientForm
from django.urls import reverse_lazy
from config.permission import ValidatePermission
from django.contrib import messages

# Create your views here.
class AddClient(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'add_client.html'
    success_url = reverse_lazy('list-client')
    url_redirect = success_url
    permission_required = 'change_client'

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
                # Mensaje de error
                return redirect('add-client')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# List Clients
class ListClient(ValidatePermission, ListView):
    model = Client
    template_name = 'list_client.html'
    permission_required = 'view_client'
    url_redirect = reverse_lazy('list-client')
    create_url = reverse_lazy('add-client')

    data = {}
    try:
        clients = Client.objects.all()

    except Exception as e:
        data['error'] = str(e)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de clientes'
        context['entity'] = 'Clientes'
        context['clients'] = Client.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context


# Update Product
class UpdateClient(ValidatePermission, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'add_client.html'
    success_url = reverse_lazy('list-client')
    url_redirect = success_url
    permission_required = 'change_client'

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
                messages.warning(request, f'Error al editar el cliente')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
# Delete Client
class DeleteClient(DeleteView, ValidatePermission):
    model = Client
    success_url = reverse_lazy('list-client')
    url_redirect = success_url
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                client_id = request.POST['client_id']
                client = Client.objects.get(pk=client_id)
                client.delete()
                messages.success(request, f'Producto eliminado: {client.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el cliente')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url

        return context