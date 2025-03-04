from django.urls import path
from . import views
from .views import CatalogView, ClothingItemDetailView

app_name = 'main'

urlpatterns = [
    # path('', views.popular_list, name='popular_list'),
    # path('<slug:slug>/',views.product_detail, name='product_detail'),
    path('', CatalogView.as_view(), name='catalog'),
    path('item/<slug:slug>/', ClothingItemDetailView.as_view(),
         name='clothing_item_detail')
]
