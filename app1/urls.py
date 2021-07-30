from django.urls import path
from app1.views import *


urlpatterns = [

    # --------------------------- Company -------------------------------
    path('',login,name='login'),
    path('lockscreen/',lockscreen,name='lockscreen'),
    path('locklogout/',locklogout,name='locklogout'),
    path('register/',register,name='register'),
    path('forgotpassword/',forgotpassword,name='forgotpassword'),
    path('changepassword/',changepassword,name='changepassword'),
    path('otp/',otp,name='otp'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('add_customer/',add_customer,name='add_customer'),
    path('view_customer/',view_customer,name='view_customer'),
    path('delete_customer/<int:id>',delete_customer,name='delete_customer'),
    path('update_customer/<int:id>',update_customer,name='update_customer'),
    path('view_order/',view_order,name='view_order'),
    path('order_accepted/<int:id>',order_accepted,name='order_accepted'),
    path('order_rejected/<int:id>',order_rejected,name='order_rejected'),
    path('view_accepted_order/',view_accepted_order,name='view_accepted_order'),
    path('invoice/<int:id>',invoice,name='invoice'),
    path('invoice_print/<int:id>',invoice_print,name='invoice_print'),
    path('order_list_p/<int:id>',order_list_p,name='order_list_p'),

    # --------------------------- Customer -------------------------------
    path('customer_login/',customer_login,name='customer_login'),
    path('customer_dashboard/',customer_dashboard,name='customer_dashboard'),
    path('customer_contact/',customer_contact,name='customer_contact'),
    path('customer_order/',customer_order,name='customer_order'),
    path('customer_profile/',customer_profile,name='customer_profile'),
    path('place_order/<int:id>',place_order,name='place_order'),
    path('customer_logout/',customer_logout,name='customer_logout'),

    # --------------------------- Product -------------------------------
    path('add_product/',add_product,name='add_product'),
    path('view_product/',view_product,name='view_product'),
    path('update_product/<int:id>',update_product,name='update_product'),
    path('delete_product/<int:id>',delete_product,name='delete_product'),
]