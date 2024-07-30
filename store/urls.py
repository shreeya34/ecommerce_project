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
    path('esewa/success/', views.esewa_success, name='esewa_success'),
    path('esewa/failure/', views.esewa_failure, name='esewa_failure'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('categories/', views.category_list_view, name='category_list_view'),
    path('categories/<slug:slug>/products/', views.category_products_view, name='category_products_view'),
    path('profile/', views.profile_view, name='profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('profile/change_password/', views.change_password_view, name='change_password'),


  
]