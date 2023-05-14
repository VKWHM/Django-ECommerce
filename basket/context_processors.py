from .basket import Basket


def basket_item_count(request, *args, **kwargs):
    return {"basketItemCount": len(Basket(request))}
