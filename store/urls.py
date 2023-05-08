from django.urls import path
from . import views
app_name = 'store'
urlpatterns = [
    path('', views.all_product, name="all_product"),
    path('item/<slug:slug>/', views.product_detail, name="product_detail")
]
