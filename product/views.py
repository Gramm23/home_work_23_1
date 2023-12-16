from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from product.forms import *
from product.models import *


class ProductListView(ListView):
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        formset = inlineformset_factory(Product, Version, form=VersionForm)(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'

    def get_success_url(self):
        return reverse_lazy('product:view', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = FormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = FormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        formset = inlineformset_factory(Product, Version, form=VersionForm)(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:index')
