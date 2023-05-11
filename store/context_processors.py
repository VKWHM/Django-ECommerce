from .models import Category


def categories(*args, **kwargs):
    return {'categories': Category.objects.all()}
