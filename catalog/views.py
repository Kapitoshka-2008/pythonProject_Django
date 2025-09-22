from django.shortcuts import render


def home_view(request):
    return render(request, 'catalog/home.html')


def contacts_view(request):
    return render(request, 'catalog/contacts.html')

# Create your views here.
