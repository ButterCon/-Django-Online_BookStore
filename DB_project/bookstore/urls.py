from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('<str:name>/home/', views.homePage, name='home'),
    path('<str:name>/<int:BookOrder_id>/order/', views.orderPage, name='order'),
    path('<str:name>/<int:book_id>/order/', views.orderConPage, name='ordercon'),
    path('<str:name>/orderdone/', views.orderdonePage, name='orderdone'),
    path('<str:name>/cart/', views.cartPage, name='cart'),
    path('<str:name>/<int:book_id>/cart/', views.cartaddPage, name='cartadd'),
    path('<str:name>/<int:Order_id>/<int:book_id>/cart/', views.cartdelPage, name='cartdel'),
    path('reg/', views.regPage, name='reg'),
    path('regCon/', views.regConPage, name='regCon'),
    path('<str:name>/userinfo/', views.userinfoPage, name='userinfo'),
    path('<str:name>/sdadd/', views.sdaddPage, name='sdadd'),
    path('<str:name>/cardadd/', views.cardaddPage, name='cardadd'),
    path('<str:name>/coupon/', views.couponPage, name='coupon'),    #회원수정->쿠폰
    path('<int:BookOrder_id>/couponselect/', views.couponselectPage, name='couponselect'),    #주문->쿠폰
    #path('<str:name>/<int:BookOrder_id>/<int:BookSB_id>/couponselectCon/', views.couponselectConPage, name='couponselectCon'),    #주문->쿠폰
    path('login/', views.loginPage, name='login'),
]