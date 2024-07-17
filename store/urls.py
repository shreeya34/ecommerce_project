from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    # path('process_order/', views.processOrder, name='process_order'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search_results, name='search_results'), 
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_image/<int:product_id>/', views.add_image, name='add_image'),

  
]