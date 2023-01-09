from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from core.document.models import Document, DocCategory
from config.permission import ValidatePermission
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, FormView
from .forms import DocumentForm, DocCategoryForm, SendFileForm
#download
import os
from config import settings as s
# Mail
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


# AddDocument
class AddDocCategory(ValidatePermission, CreateView):

    model = DocCategory
    form_class = DocCategoryForm
    template_name = 'add_doc_category.html'
    success_url = reverse_lazy('list-document-category')
    url_redirect = success_url
    permission_required = 'add_doccategory'

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Categoría'
        context['entity'] = 'Documentación'
        context['list_url'] = self.url_redirect
        context['action'] = 'add'
        return context

# List DocCategory
class ListDocCategory(ValidatePermission, ListView):
    model = DocCategory
    template_name = 'list_doc_category.html'
    url_redirect = reverse_lazy('list-document-category')
    create_url = reverse_lazy('add-document-category')

    data = {}
    try:
        categories = DocCategory.objects.all()
    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de categorías'
        context['entity'] = 'Categorías'
        context['categories'] = DocCategory.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update - Doc Category
class UpdateDocCategory(ValidatePermission, UpdateView):
    model = DocCategory
    form_class = DocCategoryForm
    template_name = 'add_doc_category.html'
    success_url = reverse_lazy('list-document-category')
    url_redirect = success_url
    permission_required = 'add_doccategory'


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
class DeleteDocCategory(ValidatePermission, DeleteView):
    model = DocCategory
    success_url = reverse_lazy('list-document-category')
    url_redirect = success_url
    permission_required = 'delete_category'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                category_id = request.POST['category_id']
                category = DocCategory.objects.get(pk=category_id)
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



# Add Document

class AddDocument(ValidatePermission, CreateView):

    model = Document
    form_class = DocumentForm
    template_name = 'add_document.html'
    success_url = reverse_lazy('list-document')
    url_redirect = success_url
    permission_required = 'add_document'


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            id_session = int(request.user.id)
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    data = form.save(user=id_session)
                else:
                    # Mensaje de error
                    data['error'] = form.errors
            else:
                # Mensaje de error
                return redirect('dashboard')

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Documento'
        context['entity'] = 'Agregar Documento'
        context['list_url'] = self.url_redirect
        context['action'] = 'add'
        return context



# List Document

class ListDocument(ValidatePermission, ListView):
    model = Document
    template_name = 'list_document.html'
    permission_required = 'view_product'
    url_redirect = reverse_lazy('list-document')
    create_url = reverse_lazy('add-document')

    data = {}
    try:
        documents = Document.objects.all()
    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de documentos'
        context['entity'] = 'Documentos'
        context['documents'] = Document.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Product
class UpdateDocument(ValidatePermission, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'add_document.html'
    success_url = reverse_lazy('list-document')
    url_redirect = success_url
    permission_required = 'change_document'

    # A traves del dispatch avisamos que existe un objeto recibido por post
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        id_session = int(request.user.id)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save(user=id_session)
            else:
                messages.warning(request, f'Error al editar el documento')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar documento'
        context['entity'] = 'Documentos'
        context['list_url'] = self.url_redirect
        context['action'] = 'edit'

        return context

# Delete Product
class DeleteDocument(ValidatePermission, DeleteView):
    model = Document
    success_url = reverse_lazy('list-document')
    url_redirect = success_url
    permission_required = 'delete_document'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                document_id = request.POST['document_id']
                document = Document.objects.get(pk=document_id)
                document.delete()
                messages.success(request, f'Documento eliminado: {document.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el documento')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Documento'
        context['entity'] = 'Documentos'
        context['list_url'] = self.success_url

        return context



# Nos muestra el navegador con posibilidad a descargarlo o imprimirlo

class DownloadFile(ValidatePermission, DetailView):
    model = Document
    success_url = reverse_lazy('list-document')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = {}
        obj = self.object
        try:
            path = str(obj.file)
            if len(path) != 0:
                file_path = os.path.join(s.MEDIA_ROOT, path)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
            else:
                messages.warning(request, 'El archivo no se ha encontrado')
                return redirect(self.success_url)
        except Exception as e:
            data['error'] = str(e)


# Envia el archivo por mail -- HACER
class SendFile(ValidatePermission, FormView):
    form_class = SendFileForm
    success_url = reverse_lazy('list-document')
    url_redirect = success_url

    def send_email(self, user, send_to, text, files):
        data = {}
        try:
            mailServer = smtplib.SMTP(s.EMAIL_HOST, s.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(s.EMAIL_HOST_USER, s.EMAIL_HOST_PASSWORD)
            mensaje = MIMEMultipart()
            mensaje['From'] = s.EMAIL_HOST_USER
            mensaje['To'] = send_to
            mensaje['Date'] = formatdate(localtime=True)
            mensaje['Subject'] = f"Documento enviado por {user.first_name} {user.last_name}"
            mensaje.attach(MIMEText(text))

            for f in files or []:
                file_path = os.path.join(s.MEDIA_ROOT, f)
                with open(file_path, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                    # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                mensaje.attach(part)

            mailServer.sendmail(s.EMAIL_HOST_USER, send_to, mensaje.as_string())
            mailServer.close()

        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.POST:
                file = []
                user = request.user
                document_id = int(request.POST['document'])
                document = Document.objects.get(pk=document_id)
                file.append(str(document.file))
                send_to = request.POST['email']
                text = request.POST['description']
                data = self.send_email(user, send_to, text, file)
                return redirect(self.success_url)
            else:
                data['error'] = 'No hay POST'
        except Exception as e:
            data['error'] = str(e)
        return data