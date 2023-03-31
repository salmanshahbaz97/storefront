
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedSimpleRouter(router, 'products', lookup = 'product')
products_router.register('product_reviews', views.ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls))
]
