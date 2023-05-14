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
        for k, v in self._basket.items():
            count += int(v['qty'])
        return count

    def add(self, item_id, count=1):
        if not self[item_id]:
            Product.products.filter(id=item_id)
            self._basket[item_id] = {'price': str(Product.products.filter(
                id=item_id)[0].price), 'qty': count}
        else:
            self[item_id]['qty'] += count
        self.save()

    def save(self):
        self.session.modified = True
