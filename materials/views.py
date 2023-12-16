from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from materials.models import Material


class MaterialsListView(ListView):
    model = Material


class MaterialsDetailView(DetailView):
    model = Material

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialsCreateView(CreateView):
    model = Material
    fields = ('title', 'body', 'image')
    success_url = reverse_lazy('materials:material_list')

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)


class MaterialsUpdateView(UpdateView):
    model = Material
    fields = ('title', 'body', 'image',)

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:material_detail', args=(self.kwargs.get('pk'),))


class MaterialsDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials:material_list')
