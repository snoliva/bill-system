from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UMForm, ProductoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from bases.views import SinPrivilegios
# Create your views here.

class CategoriaView(SinPrivilegios, ListView):
    #Propertie PermissionRequiredMixin
    permission_required = "inv.view_categoria"
    #
    model = Categoria
    template_name = 'inv/categoria_list.html'
    context_object_name = 'obj'
    #login_url = 'bases:login'

class CategoriaNew(SuccessMessageMixin, SinPrivilegios, CreateView):
    model = Categoria
    template_name = 'inv/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')
    login_url = 'bases:login'
    #Propiedad SuccessMessageMixin
    success_message = "Categoría creada satisfactoriamente"
    #Propertie PermissionRequiredMixin
    permission_required = "inv.add_categoria"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin, SinPrivilegios, UpdateView):
    model = Categoria
    template_name = 'inv/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_url = reverse_lazy('inv:categoria_list')
    #login_url = 'bases:login'
    #Propiedad SuccessMessageMixin
    success_message = "Categoría actualizada satisfactoriamente"
    #Propertie PermissionRequiredMixin
    permission_required = "inv.change_categoria"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class CategoriaDel(SinPrivilegios, DeleteView):
    model = Categoria
    template_name = 'inv/categoria_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inv:categoria_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.delete_categoria"

class SubCategoriaView(SinPrivilegios, ListView):
    #Propertie PermissionRequiredMixin
    permission_required = "inv.view_subcategoria"
    #
    model = SubCategoria
    template_name = 'inv/subcategoria_list.html'
    context_object_name = 'obj'
    #login_url = 'bases:login'

class SubCategoriaNew(SinPrivilegios, CreateView):
    model = SubCategoria
    template_name = 'inv/subcategoria_form.html'
    context_object_name = 'obj'
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.add_subcategoria"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class SubCategoriaEdit(SinPrivilegios, UpdateView):
    model = SubCategoria
    template_name = 'inv/subcategoria_form.html'
    context_object_name = 'obj'
    form_class = SubCategoriaForm
    success_url = reverse_lazy('inv:subcategoria_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.change_subcategoria"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class SubCategoriaDel(SinPrivilegios, DeleteView):
    model = SubCategoria
    template_name = 'inv/categoria_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inv:subcategoria_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.delete_subcategoria"

class MarcaView(SinPrivilegios, ListView):
    #Propertie PermissionRequiredMixin
    permission_required = "inv.view_marca"

    model = Marca
    template_name = 'inv/marca_list.html'
    context_object_name = 'obj'
    #login_url = 'bases:login'

class MarcaNew(SinPrivilegios, CreateView):
    model = Marca
    template_name = 'inv/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy('inv:marca_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.add_marca"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class MarcaEdit(SinPrivilegios, UpdateView):
    model = Marca
    template_name = 'inv/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy('inv:marca_list')
    #Propertie PermissionRequiredMixin
    permission_required = "inv.change_marca"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    context = {}
    template_name = 'inv/catalogo_del.html'

    if not marca:
        return redirect('inv:marca_list')
    
    if request.method == 'GET':
        context = {'obj':marca}

    if request.method == 'POST':
        marca.estado = False
        marca.save()
        messages.success(request, 'Marca Inactivada')
        return redirect('inv:marca_list')

    return render(request, template_name, context)

class UMView(SinPrivilegios, ListView):
    model = UnidadMedida
    template_name = 'inv/um_list.html'
    context_object_name = 'obj'
    #Propertie PermissionRequiredMixin
    permission_required="inv.view_unidadmedida"
    #login_url = 'bases:login'

class UMNew(SinPrivilegios, CreateView):
    model = UnidadMedida
    template_name = 'inv/um_form.html'
    context_object_name = 'obj'
    form_class = UMForm
    success_url = reverse_lazy('inv:um_list')
    #Propertie PermissionRequiredMixin
    permission_required="inv.add_unidadmedida"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class UMEdit(SinPrivilegios, UpdateView):
    model = UnidadMedida
    template_name = 'inv/um_form.html'
    context_object_name = 'obj'
    form_class = UMForm
    success_url = reverse_lazy('inv:um_list')
    #Propertie PermissionRequiredMixin
    permission_required="inv.change_unidadmedida"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('inv.change_unidadmedida', login_url='bases:sin_privilegios')
def um_inactivar(request, id):
    um = UnidadMedida.objects.filter(pk=id).first()
    context = {}
    template_name = 'inv/catalogo_del.html'

    if not um:
        return redirect('inv:um_list')
    
    if request.method == 'GET':
        context = {'obj':um}

    if request.method == 'POST':
        um.estado = False
        um.save()
        return redirect('inv:um_list')

    return render(request, template_name, context)

class ProductoView(SinPrivilegios, ListView):
    model = Producto
    template_name = 'inv/producto_list.html'
    context_object_name = 'obj'
    #Propertie PermissionRequiredMixin
    permission_required="inv.view_producto"
    #login_url = 'bases:login'

class ProductoNew(SinPrivilegios, CreateView):
    model = Producto
    template_name = 'inv/producto_form.html'
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy('inv:producto_list')
    #Propertie PermissionRequiredMixin
    permission_required="inv.add_producto"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ProductoEdit(SinPrivilegios, UpdateView):
    model = Producto
    template_name = 'inv/producto_form.html'
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy('inv:producto_list')
    #Propertie PermissionRequiredMixin
    permission_required="inv.change_producto"
    #login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('inv.change_producto', login_url='bases:sin_privilegios')
def producto_inactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    context = {}
    template_name = 'inv/catalogos_del.html'

    if not prod:
        return redirect('inv:producto_list')
    
    if request.method == 'GET':
        context = {'obj':prod}

    if request.method == 'POST':
        prod.estado = False
        prod.save()
        return redirect('inv:producto_list')

    return render(request, template_name, context)
