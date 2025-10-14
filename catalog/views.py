from django.shortcuts import render, get_object_or_404
from .models import Product


def home_view(request):
    products = Product.objects.select_related('category').all()
    context = {
        'products': products,
    }
    return render(request, 'catalog/home.html', context)


def contacts_view(request):
    return render(request, 'catalog/contacts.html')

def product_detail_view(request, pk: int):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)
