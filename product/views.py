from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from product.forms import *
from product.models import *


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['product_list']

        active_versions_per_product = {product.id: Version.objects.filter(product=product, active=True).first() for
                                       product in products}
        context['active_versions'] = active_versions_per_product

        return context


class ProductDetailView(DetailView):
    model = Product


@login_required
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            question = request.POST.get('question')
            print(f'Имя: {first_name}, email: ({email}), Вопрос {question}')
            return redirect('product:contacts')
    else:
        form = ContactForm()
    return render(request, 'product/contacts.html', {'form': form})


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product:index')
    permission_required = 'product.add_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
            for form in context_data['formset']:
                if not self.request.user.is_staff:
                    form.fields['active'].widget = forms.HiddenInput()

        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        formset = inlineformset_factory(Product, Version, form=VersionForm)(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            del form.fields['active']

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        formset = VersionFormset()
        for subform in formset.forms:
            if not self.request.user.is_staff:
                del subform.fields['active']
        return form

    def test_func(self):
        return not self.request.user.is_staff


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    permission_required = 'product.change_product'

    def get_success_url(self):
        return reverse_lazy('product:view', args=[self.object.pk])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            del form.fields['active']
        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = FormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = FormSet(instance=self.object)
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:index')

    def test_func(self):
        return self.request.user.is_superuser
