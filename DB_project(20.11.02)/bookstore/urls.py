from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path('<str:name>/home/', views.homePage, name='home'),
    path('<str:name>/<int:book_id>/sinorder/', views.sinOrderPage, name='sinorder'),
    path('<str:name>/mulorder/', views.mulOrderPage, name='mulorder'),
    path('<str:name>/cart/', views.cartPage, name='cart'),
    path('<str:name>/<int:book_id>/cartadd/', views.cartaddPage, name='cartadd'),
    path('<str:name>/<int:book_id>/cartdel/', views.cartdelPage, name='cartdel'),
    path('reg/', views.regPage, name='reg'),
    path('regCon/', views.regConPage, name='regCon'),
    path('<str:name>/userinfo/', views.userinfoPage, name='userinfo'),
    path('<str:name>/sdadd/', views.sdaddPage, name='sdadd'),
    path('<str:name>/cardadd/', views.cardaddPage, name='cardadd'),
    path('login/', views.loginPage, name='login'),
]