from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from .models import Proveedor, ComprasDet, ComprasEnc
from cmp.forms import ProveedorForm, ComprasEncForm

from inv.models import Producto

from django.contrib.auth.decorators import login_required, permission_required

from bases.views import SinPrivilegios

import datetime
# Create your views here.

class ProveedorView(SinPrivilegios, ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    #Propertie PermissionRequiredMixin
    permission_required="cmp.view_proveedor"
    #login_url = "bases:login"

class ProveedorNew(SinPrivilegios, CreateView):
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
     #Propertie PermissionRequiredMixin
    permission_required="cmp.add_proveedor"
    #login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class ProveedorEdit(SinPrivilegios, UpdateView):
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
     #Propertie PermissionRequiredMixin
    permission_required="cmp.change_proveedor"
    #login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('cmp.change_proveedor', login_url='bases:sin_privilegios')
def proveedorInactivar(request, id):
    template_name = 'cmp/inactivar_prv.html'
    contexto = {}
    print(id)
    prv = Proveedor.objects.get(pk=id)

    print(prv.descripcion)

    if not prv:
        return HttpResponse('Proveedor no existe '+str(id))

    if request.method == 'GET':
        contexto = {
            'obj' : prv,
        }
        print(contexto)
    if request.method == 'POST':
        prv.estado = False
        prv.save()
        contexto = {
            'obj': 'OK'
        }
        return HttpResponse('Proveedor Inactivado')

    return render(request, template_name, contexto)

class ComprasView(SinPrivilegios, ListView):
    model = ComprasEnc
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    permission_required = "cmp.view_comprasenc"


@login_required(login_url="/login/")
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request, compra_id=None):
    template_name = "cmp/compras.html"
    prod = Producto.objects.filter(estado=True)
    form_compras = {}
    contexto ={}

    if request.method == "GET":
        form_compras = ComprasEncForm
        enc = ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = ComprasDet.objects.filter(compras = enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total':enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det=None
        
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras}

    return render(request, template_name, contexto)