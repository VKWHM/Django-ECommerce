from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .basket import Basket
import json


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket, 'total_price': basket.get_total_price()})


class BasketAPI(View):
    def get(self, request, id):
        basket = Basket(request)
        if basket[id]:
            return JsonResponse(basket[id])
        return JsonResponse({}, status=404)

    def post(self, request, id):
        qty = max(1, int(request.POST.get('qty', 1)))
        basket = Basket(request)
        basket.add(id, qty)
        return JsonResponse({'basket_item_count': len(basket)})

    def delete(self, request, id):
        basket = Basket(request)
        if basket.delete(id):
            return JsonResponse({'basket_item_count': len(basket), 'item_id': id, 'total_price': basket.get_total_price()})
        return JsonResponse({},status=404)

    def patch(self, request, id):
        basket = Basket(request)
        if basket[id]:
            qty = max(0, int(json.loads(request.body).get('qty', False)))
            if qty:
                basket[id]['qty'] = qty
                return JsonResponse({'basket_item_count': len(basket), 'item_id': id, 'total_price': basket.get_total_price()})
            else:
                return JsonResponse({}, status=400)
        else:
            return JsonResponse({}, status=404)
