from django.urls import path
from . import views
from django.conf.urls import url  

urlpatterns = [
    path('', views.index),
    path('main', views.main),
    path('customer/next', views.next),
    path('customer/dashboard', views.dashboard),
    path('customer/loginpage', views.loginpage),
    path('customer/register', views.register),
    path('customer/login', views.login),
    path('customer/logout', views.logout),
    path('customer/addpoints', views.addpoints),
    path('customer/addpoints2', views.addpoints2),
    path('customer/logindash', views.logindash),
    path('customer/edit/<int:id>', views.edit),
    path('customer/update/<int:id>', views.update),
    path('admin/edit/<int:id>', views.adminedit),
    path('admin/manage_newsletter', views.manage_newsletter),
    path('admin/add_newsletter', views.add_newsletter),
    path('admin/manage_customers', views.manage_customers),
    path('admin/delete_cust/<int:id>', views.delete_cust),
]