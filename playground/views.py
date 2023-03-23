from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Order, OrderItem


def say_hello(request):
    try:
        send_mail('subject', 'sending email from fake smtp server' , 'salmanshahbaz97@gmail.com', ['salmanshahbaz97@gmail.com'])
    except BadHeaderError:
        pass
    products = list(Product.objects.filter(unit_price__lt=20, inventory__lt=10)) 

    queryset = Order.objects.select_related('customer').all()
    expensive = Product.objects.latest('inventory')
    cheapest = Product.objects.earliest('inventory')

    products = Product.objects.all()
    return render(request, 'index.html', {'name': 'salman shahbaz', 'orders': list(queryset), 'expensive': expensive, 'cheapest': cheapest})
    
