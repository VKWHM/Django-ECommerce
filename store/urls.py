from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.product_all, name="all_product"),
    path('products/<slug:slug>/', views.product_detail, name="product_detail"),
    path('categories/<slug:category_slug>/',
         views.category_list, name='category_list'),
]
