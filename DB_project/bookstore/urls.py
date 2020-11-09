from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('<str:name>/home/', views.homePage, name='home'),
    ############################주문####################################
    path('<str:name>/order/', views.orderPage, name='order'),
    path('<str:name>/<int:book_id>/order/', views.orderConPage, name='ordercon'),
    path('<str:name>/orderdone/', views.orderdonePage, name='orderdone'),
    ############################장바구니#################################
    path('<str:name>/cart/', views.cartPage, name='cart'),
    path('<str:name>/<int:book_id>/cart/', views.cartaddPage, name='cartadd'),
    path('<str:name>/<int:book_id>/cart/', views.cartdelPage, name='cartdel'),
    ############################회원가입#################################
    path('reg/', views.regPage, name='reg'),
    path('regCon/', views.regConPage, name='regCon'),
    ############################회원정보수정##############################
    path('<str:name>/userinfo/', views.userinfoPage, name='userinfo'),
    path('<str:name>/sdadd/', views.sdaddPage, name='sdadd'),
    path('<str:name>/cardadd/', views.cardaddPage, name='cardadd'),
    ############################쿠폰####################################
    path('<str:name>/coupon/', views.couponPage, name='coupon'),    #회원수정->쿠폰
    path('<int:BookOrder_id>/couponselect/', views.couponselectPage, name='couponselect'),    #주문->쿠폰
]