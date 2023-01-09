from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from config.permission import ValidatePermission
from core.product.models import Product
from core.sales.models import Sale, SaleProduct
from core.stock.models import Lot, LotProduct
from core.user.models import User
from core.user.forms import UserForm, ProfileForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
from django.contrib import messages

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    current_year = datetime.now().year
    current_month = datetime.now().month

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        year = self.current_year
        month = self.current_month
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                points = []
                for m in range(1, 13):
                    total = Sale.objects.filter(date_sale__year=year, date_sale__month=m).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    points.append(float(total))
                data = {
                    'data': points
                }
            elif action == 'get_graph_sales_products_year_month':
                points = []
                for p in Product.objects.filter():
                    total = SaleProduct.objects.filter(sale__date_sale__year=year, sale__date_sale__month=month, product_id=p.id).aggregate(result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
                    if total > 0:
                        points.append({'name': p.name,'y': float(total)})
                data = {
                    'data': points
                }
            elif action == 'get_graph_buy_products_year_month':
                points = []
                for p in Product.objects.filter():
                    total = LotProduct.objects.filter(lot__lot_date__year=year, lot__lot_date__month=month, product_id=p.id).aggregate(result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
                    if total > 0:
                        points.append({'name': p.name,'y': float(total)})
                data = {
                    'data': points
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['title'] = 'Dashboard'
        context['year'] = self.current_year
        context['month'] = self.current_month
        return context


# Page not found
def page_not_found404(request, exception):
    return render(request, '404.html')

#Create User
class CreateUser(ValidatePermission, CreateView):
    model = User
    form_class = UserForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('list-user')
    url_redirect = success_url
    permission_required = 'add_user'

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
                return redirect('add-user')

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# Lista
class ListUser(ValidatePermission, ListView):
    model = User
    template_name = 'list_user.html'
    permission_required = 'view_user'
    url_redirect = reverse_lazy('list-user')
    create_url = reverse_lazy('add-user')

    data = {}
    try:
        users = User.objects.all()
    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.url_redirect
        context['users'] = User.objects.all()
        context['create_url'] = self.create_url
        return context

# Update User
class UpdateUser(ValidatePermission, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('list-user')
    url_redirect = success_url
    permission_required = 'change_user'

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
                messages.warning(request, f'Error al editar el usuario')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Delete User
class DeleteUser(DeleteView, ValidatePermission):
    model = User
    success_url = reverse_lazy('list-user')
    url_redirect = success_url
    permission_required = 'delete_user'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                user_id = request.POST['user_id']
                user = User.objects.get(pk=user_id)
                user.delete()
                messages.success(request, f'Usuario eliminado: {user.username}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el usuario')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url

        return context

# Change Password
class UserChangePassword(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Select Group
class SelectGroup(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('dashboard'))

# Update Profile
class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

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
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
