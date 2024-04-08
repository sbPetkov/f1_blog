from f1_blog.merchandise.models import Merchandise


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if "session_key" not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, item, quantity):
        item_id = str(item.id)
        item_qty = str(quantity)
        if item_id in self.cart:
            pass
        else:
            self.cart[item_id] = int(item_qty)
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        item_ids = self.cart.keys()
        products = Merchandise.objects.filter(id__in=item_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, item, quantity):
        item_id = str(item)
        item_qty = int(quantity)
        our_cart = self.cart
        our_cart[item_id] = item_qty
        self.session.modified = True
        updated_cart = self.cart
        return updated_cart

    def delete(self, item):
        item_id = str(item)
        if item_id in self.cart:
            del self.cart[item_id]
        self.session.modified = True

    def total(self):
        item_id = self.cart.keys()
        items = Merchandise.objects.filter(id__in=item_id)
        quantity = self.cart
        total_price = 0
        for key, value in quantity.items():
            key = int(key)
            for item in items:
                if item.id == key:
                    total_price += item.price * value
        return total_price
