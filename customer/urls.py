from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.Customers.as_view()),
    path('customer/', views.SingleCustomer.as_view()),
    path('search-customers/', views.SearchCustomer.as_view()),
    path('customer/<int:id>', views.SingleCustomer.as_view()),
    path('remove-customers/', views.RemoveMultiCustomers.as_view()),
]
