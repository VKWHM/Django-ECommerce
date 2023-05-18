from decimal import Decimal

from store.models import Product


class Basket:
    def __init__(self, request):

        self.session = request.session
        if not self.session.get('sessionKey', False):
            self.session['sessionKey'] = {}
        self._basket = self.session.get('sessionKey')

    def __getitem__(self, item):
        return self._basket.get(item, dict())

    def __len__(self):
        count = 0
        for item in self._basket.values():
            count += int(item['qty'])
        return count

    def __iter__(self):
        for product in Product.products.filter(id__in=self._basket.keys()):
            item = self._basket[str(product.id)]
            item['product'] = product
            yield item

    def add(self, item_id, count=1):
        if not self[item_id]:
            Product.products.filter(id=item_id)
            self._basket[item_id] = {'price': str(Product.products.filter(
                id=item_id)[0].price), 'qty': count}
        else:
            self[item_id]['qty'] += count
        self.save()

    def delete(self, item_id):
        if item_id in self._basket.keys():
            del self._basket[item_id]
            self.save()
            return True
        return False

    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['qty']) for item in self._basket.values())

    def save(self):
        self.session.modified = True
