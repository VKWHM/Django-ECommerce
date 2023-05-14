from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .basket import Basket


def basket_summary(request):
    return render(request, 'store/basket/summary.html')


class BasketAPI(View):
    def get(self, request, id):
        basket = Basket(request)
        return JsonResponse(basket[id], status=200 if basket[id] else 404)

    def post(self, request, id):
        qty = max(1, int(request.POST.get('qty', 1)))
        basket = Basket(request)
        basket.add(id, qty)
        return JsonResponse({'basket_item_count': len(basket)})
