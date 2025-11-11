from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.select_related('category').filter(status=Product.PublicationStatus.PUBLISHED)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('category')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        return product.owner_id == self.request.user.id


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        # owner can delete; moderators (with delete permission) can delete any
        product = self.get_object()
        user = self.request.user
        return product.owner_id == user.id or user.has_perm('catalog.delete_product')


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    if product.status == Product.PublicationStatus.PUBLISHED:
        product.status = Product.PublicationStatus.DRAFT
        product.save(update_fields=['status'])
    # redirect back to product detail if available; otherwise to home
    return redirect('catalog:product_detail', pk=product.pk)
