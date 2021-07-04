from django.urls import path
from . import views

urlpatterns = [
    path('sale/', views.SingleSale.as_view()),
    path('sales/', views.Sales.as_view()),
    path('sale-products/', views.SaleProducts.as_view()),
    path('payment/', views.SingleOrderPayment.as_view()),
    path('sale-reports/', views.SaleReport.as_view()),
    path('remove-sale-product/', views.SingleSaleProduct.as_view()),


]
