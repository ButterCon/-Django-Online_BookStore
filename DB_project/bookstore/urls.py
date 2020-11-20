from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('test1/', views.test1, name='test1'),
    path('test2/', views.test2, name='test2'),
    ############################회원가입#################################
    path('reg/', views.regPage, name='reg'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:User_id>/home/', views.homePage, name='home'),
    ############################주문####################################
    path('order/', views.orderPage, name='order'),
    path('CPorder/', views.CPorderPage, name='CPorder'),
    path('orderdone/', views.orderdonePage, name='orderdone'),
    ############################장바구니#################################
    path('cart/', views.cartPage, name='cart'),
    path('<int:book_id>/mulcartadd/', views.mulcartaddPage, name='mulcartadd'),
    path('<int:book_id>/sincartadd/', views.sincartaddPage, name='sincartadd'),
    path('<int:book_id>/cartdel/', views.cartdelPage, name='cartdel'),
    ############################회원정보수정##############################
    path('userinfo/', views.userinfoPage, name='userinfo'),
    path('sdadd/', views.sdaddPage, name='sdadd'),
    path('cardadd/', views.cardaddPage, name='cardadd'),
    ############################쿠폰####################################
    path('coupon/', views.couponPage, name='coupon'),    #회원수정->쿠폰
    path('<int:BookOrder_id>/couponselect/', views.couponselectPage, name='couponselect'),    #주문->쿠폰
    path('<int:BookOrder_id>/<int:CP_id>/cpcancel/', views.cpcancelPage, name="cpcancel"),     #쿠폰 선택 취소 페이지
    path('<int:BookOrder_id>/<int:CP_id>/couponDC/', views.CouponDCpage, name='couponDC'),    #쿠폰 할인 값 넣기
    ############################동서페이####################################
    path('DPref/', views.DP_ref, name='DPref'),    #동서페이 조회
    path('DPissue/', views.DP_issue, name='DPissue'),    #동서페이 발급
    path('DPcharge/', views.DP_charege, name='DPcharge'),    #동서페이 충전
    path('DPdel/', views.DP_del, name='DPdel'),    #동서페이 해지
]