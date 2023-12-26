from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from django.http import Http404
from materials.models import Material
from users.models import User


class MaterialsListView(LoginRequiredMixin, ListView):
    model = Material


class MaterialsDetailView(DetailView):
    model = Material

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Material
    fields = ('title', 'body', 'image')
    success_url = reverse_lazy('materials:material_list')
    permission_required = 'materials.add_material'

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(self.request.user)
        self.object = form.save()
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class MaterialsUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    fields = ('title', 'body', 'image', 'is_publish',)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            del form.fields['is_publish']
        else:
            for field_name in ['title', 'image']:
                del form.fields[field_name]
        return form

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        staff_list = User.objects.filter(is_staff=True)
        if self.request.user in staff_list:
            return self.object
        elif self.request.user == self.object.user:
            return self.object
        else:
            raise Http404("Вы не являетесь владельцем этого товара")

    def get_success_url(self):
        return reverse('materials:material_detail', args=(self.kwargs.get('pk'),))


class MaterialsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('materials:material_list')
    permission_required = 'materials.delete_material'
