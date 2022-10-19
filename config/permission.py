from crum import get_current_request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from core.company.models import Company

class ValidatePermission(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('dashboard')
        return self.url_redirect

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    return redirect('dashboard')
            return super().get(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return redirect(self.get_url_redirect())


class ExistsCompany(object):
    def dispatch(self, request, *args, **kwargs):
        if Company.objects.all().exists():
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No se puede facturar si no esta registrada la compañia')
        return redirect('dashboard')