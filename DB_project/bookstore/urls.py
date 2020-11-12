from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('test1/', views.test1, name='test1'),
    path('test2/', views.test2, name='test2'),
    ############################회원가입#################################
    path('reg/', views.regPage, name='reg'),
    path('login/', views.login, name='login'),
    path('<int:User_id>/home/', views.homePage, name='home'),
    ############################주문####################################
    path('<int:Order_id>/order/', views.orderPage, name='order'),
    path('<int:Order_id>/CPorder/', views.CPorderPage, name='CPorder'),
    path('<int:Book_id>/sinorder/', views.sinorderPage, name='sinorder'),
    path('orderdone/', views.orderdonePage, name='orderdone'),
    ############################장바구니#################################
    path('cart/', views.cartPage, name='cart'),
    path('<int:book_id>/cartadd/', views.cartaddPage, name='cartadd'),
    path('<int:book_id>/cartdel/', views.cartdelPage, name='cartdel'),
    ############################회원정보수정##############################
    path('userinfo/', views.userinfoPage, name='userinfo'),
    path('sdadd/', views.sdaddPage, name='sdadd'),
    path('cardadd/', views.cardaddPage, name='cardadd'),
    ############################쿠폰####################################
    path('coupon/', views.couponPage, name='coupon'),    #회원수정->쿠폰
    path('<int:BookOrder_id>/couponselect/', views.couponselectPage, name='couponselect'),    #주문->쿠폰
    path('<int:BookOrder_id>/<int:coupon_id>/couponDC/', views.CouponDCpage, name='couponDC'),    #쿠폰 할인 값 넣기
    ############################동서페이####################################
    path('DPserch/', views.DPserchpage, name='DPserch'),    #동서페이 조회
]