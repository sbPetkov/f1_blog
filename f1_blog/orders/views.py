from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from f1_blog.cart.cart import Cart
from f1_blog.orders.models import Order, OrderItem

def order_create_view(request):
    if request.method == 'POST':
        form_data = request.POST
        full_name = ""
        if 'first_name' in form_data and 'last_name' in form_data:
            full_name = form_data.get('first_name') + ' ' + form_data.get('last_name')

        order = Order.objects.create(
            full_name=full_name,
            email=form_data.get('email'),
            phone_number=form_data.get('phone_number'),
            address=form_data.get('address'),
            status=Order.PENDING
        )

        cart = Cart(request)
        cart_products = cart.get_products()
        cart_quantities = cart.get_quants()

        for item in cart_products:
            quantity = cart_quantities.get(str(item.id), 0)
            OrderItem.objects.create(order=order, merchandise=item, quantity=quantity)

        cart.clear()

        return redirect('index')


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Order.objects.order_by('-status', '-created_at')


class OrderDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order'
    permission_required = 'orders.view_order_list'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = order.items.all()
        context['total_price'] = sum(item.subtotal() for item in order.items.all())
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = Order.COMPLETED
        order.save()
        return redirect(reverse('order-list'))


