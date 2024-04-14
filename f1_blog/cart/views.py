from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages

from ..merchandise.models import Merchandise


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    totals = cart.total()

    user_info = {}

    if request.user.is_authenticated:
        user = request.user
        user_info = {
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name,
            'email': user.profile.email,
            'address': user.profile.address,
            'phone_number': user.profile.phone_number
        }

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'user_info': user_info
    }
    return render(request, 'cart_summery/cart_summery.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
        item = get_object_or_404(Merchandise, id=item_id)
        cart.add(item=item, quantity=item_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, 'Product added successfully!')
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        cart.delete(item=item_id)
        response = JsonResponse({'item': item_id})
        messages.success(request, 'Item deleted successfully!')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))

        cart.update(item=item_id, quantity=item_qty)
        response = JsonResponse({'qty': item_qty})
        messages.success(request, f'Product updated successfully!')
        return response

