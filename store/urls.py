
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>', views.product_detail),

    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view(), name="collection-detail"),

]