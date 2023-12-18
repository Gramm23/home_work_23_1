from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
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


@method_decorator(login_required, name='dispatch')
class MaterialsCreateView(CreateView):
    model = Material
    fields = ('title', 'body', 'image')
    success_url = reverse_lazy('materials:material_list')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404("Вы не аутентифицированы")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MaterialsUpdateView(UpdateView):
    model = Material
    fields = ('title', 'body', 'image',)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("Вы не имеете права редактировать этот материал")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:material_detail', args=(self.kwargs.get('pk'),))


@method_decorator(login_required, name='dispatch')
class MaterialsDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials:material_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("Вы не имеете права удалять этот материал")
        return super().dispatch(request, *args, **kwargs)
