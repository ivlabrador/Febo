from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import UpdateView, CreateView
from .models import Company
from .forms import CompanyForm
from django.urls import reverse_lazy
from config.permission import ValidatePermission

class CreateCompany(ValidatePermission, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'add_company.html'
    success_url = reverse_lazy('dashboard')
    url_redirect = success_url
    permission_required = 'change_company'

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

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
                return redirect('dashboard')

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar compañía'
        context['entity'] = 'Registrar Compañía'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


# Update Product
class UpdateCompany(ValidatePermission, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'add_company.html'
    success_url = reverse_lazy('dashboard')
    url_redirect = success_url
    permission_required = 'change_company'

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
                messages.warning(request, f'Error al editar la compañía')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar compañía'
        context['entity'] = 'Compañía'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context