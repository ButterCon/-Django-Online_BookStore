from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('<str:name>/home/', views.homePage, name='home'),
    ############################주문####################################
    path('<str:name>/<int:Order_id>/order/', views.orderPage, name='order'),
    path('<str:name>/<int:Order_id>/CPorder/', views.CPorderPage, name='CPorder'),
    path('<str:name>/<int:Book_id>/sinorder/', views.sinorderPage, name='sinorder'),
    path('<str:name>/<int:Order_id>/orderdone/', views.orderdonePage, name='orderdone'),
    path('<str:name>/<int:BookOrder_id>/dpuse/', views.dpusePage, name='dpuse'),
    ############################장바구니#################################
    path('<str:name>/<int:Order_id>/cart/', views.cartPage, name='cart'),
    path('<str:name>/<int:book_id>/<int:Order_id>/cartadd/', views.cartaddPage, name='cartadd'),
    path('<str:name>/<int:book_id>/<int:Order_id>/cartdel/', views.cartdelPage, name='cartdel'),
    ############################회원가입#################################
    path('reg/', views.regPage, name='reg'),
    path('regCon/', views.regConPage, name='regCon'),
    ############################회원정보수정##############################
    path('<str:name>/userinfo/', views.userinfoPage, name='userinfo'),
    path('<str:name>/sdadd/', views.sdaddPage, name='sdadd'),
    path('<str:name>/cardadd/', views.cardaddPage, name='cardadd'),
    path('<str:name>/dpserch/', views.dpserchPage, name='dpserch'),
    ############################쿠폰####################################
    path('<str:name>/coupon/', views.couponPage, name='coupon'),    #회원수정->쿠폰
    path('<str:name>/<int:BookOrder_id>/couponselect/', views.couponselectPage, name='couponselect'),    #주문->쿠폰
    path('<str:name>/<int:BookOrder_id>/<int:coupon_id>/couponDC/', views.CouponDCpage, name='couponDC'),    #쿠폰 할인 값 넣기
]