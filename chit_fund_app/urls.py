from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'), 
    path('home/', views.home, name='home'),  # Home page
    # Subscribers
    path('subscribers/', views.list_subscribers,name='list_subscribers'),
    path('subscribers/add/', views.add_subscriber),
    path('subscribers/edit/<int:id>/', views.edit_subscriber),
    path('subscribers/delete/<int:id>/', views.delete_subscriber, name='delete_subscriber'),

    # Chit Groups
    path('chit_groups/', views.list_chit_groups,name='list_chit_groups'),
    path('chit_groups/add/', views.add_chit_group),
    path('chit_groups/edit/<int:id>/', views.edit_chit_group),
    path('chit_groups/delete/<int:id>/', views.delete_chit_group, name='delete_chit_group'),

    # Payments
    path('payments/', views.list_payments,name='list_payments'),
    path('payments/add/', views.add_payment),
    path('payments/edit/<int:id>/', views.edit_payment, name='edit_payment'),
    path('payments/delete/<int:id>/', views.delete_payment, name='delete_payment'),
]
