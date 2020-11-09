from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from .models import User
from .models import ShippingDestination
from .models import ShoppingBasket
from .models import Card
from .models import Order
from .models import Book
from .models import BookSB
from .models import BookOrder
from .models import Coupon
import datetime

# Create your views here.
def loginPage(request):
    if request.method == "POST":
        id_temp = request.POST['id']
        pw_temp = request.POST['pw']
        try:
            User_qs = User.objects.get(User_id=id_temp)
            if id_temp == User_qs.User_id and pw_temp == User_qs.User_pw:
                print("계정 일치")
                context = {'User': User_qs}
                return render(request, 'bookstore/loginPage.html', context)
            else:
                print("계정 불일치 try")
            return HttpResponse('계정 불일치')
        except:
            return HttpResponse('아이디 혹은 비밀번호가 존재하지 않습니다.')
    else:
        return render(request, 'bookstore/loginPage.html')


def homePage(request, name):
    User_qs = User.objects.get(User_name=name)
    Book_qs = Book.objects.all()
    #Order 생성                   !!!!!!꼭 cart들어갔다 나가면 삭제해야됨 !!!!!!!!
    Order_qs = Order(User=User_qs)
    Order_qs.save()
    context = {'User': User_qs, 'Book_list': Book_qs, 'Order_id': Order_qs.id}  #주문 id 저장하기
    return render(request, 'bookstore/homePage.html', context)


def cartPage(request, name, Order_id):
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    #총가격
    total = 0
    for i in BookSB_qs:
        total += i.Book.Book_price
    context = {'User': User_qs, 'BookSB_list': BookSB_qs, 'Order_id': Order_id, 'Book_total_price': total}
    return render(request, 'bookstore/cartPage.html', context)


def cartaddPage(request, name, book_id, Order_id):
    # 홈에서 장바구니 클릭시 이벤트
    # 책 재고량 -1
    # 책 재고량 수정하고 나머지는 orderCon이라 같음
    # User 장바구니에 Book 추가됨
    User_qs = User.objects.get(User_name=name)
    Book_qs = Book.objects.get(id=book_id)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    #책 stock -1 해주기
    Book_qs.Book_stock += -1
    Book_qs.save()
    #장바구니에 책 넣기
    BookSB(Book=Book_qs, ShoppingBasket=SB_qs).save()
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs) #장바구니 가져오기
    #총가격
    total = 0
    for i in BookSB_qs:
        total += i.Book.Book_price
    context = {'User': User_qs, 'BookSB_list': BookSB_qs, 'Book_total_price': total, 'Order_id': Order_id}
    return render(request, 'bookstore/cartPage.html', context)


def cartdelPage(request, name, book_id, Order_id):
    #장바구니 페이지에서 장바구니 지우기 클릭시 이벤트
    #책 재고량 +1
    #User 장바구니에 Book 제거
    User_qs = User.objects.get(User_name=name)
    Book_qs = Book.objects.get(id=book_id)  #지워야하는 책 쿼리 가져옴
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    # 책 stock +1 해주기
    Book_qs.Book_stock += 1
    Book_qs.save()
    #유저장바구니리스트(BookSB)에 책 빼주기 -1
    BookSB_qs = BookSB.objects.filter(Book=Book_qs) #장바구니에서 지워줄 책리스트 가져오기
    BookSB_qs.last().delete()  #장바구니에 책 지워줌
    #총가격
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    total = 0
    for i in BookSB_qs:
        total += i.Book.Book_price
    context = {'User': User_qs, "BookSB_list": BookSB_qs, 'Book_total_price': total, 'Order_id': Order_id}
    return render(request, 'bookstore/cartPage.html', context)


def orderPage(request, name, Order_id):
    User_qs = User.objects.get(User_name=name)
    SD_qs = ShippingDestination.objects.filter(User=User_qs).first()
    Card_qs = Card.objects.filter(User=User_qs).first()
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    Order_qs = Order.objects.get(id=Order_id)
    total_price = 0 #총 금액
    for i in BookSB_qs:
        total_price += i.Book.Book_price  #모든 책 가격 더하기
        Order_qs.save()
        print(Order_qs.Order_totalprice)
        qs = BookOrder(Book=i.Book, Order=Order_qs, BO_count=1, BO_price=i.Book.Book_price)
        qs.save()
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)
    for i in BookOrder_qs:
        for j in BookOrder_qs:
            if i.id != j.id:
                if i.Book.id == j.Book.id:
                    j.delete()
                    i.BO_count += 1
                    i.BO_price += i.Book.Book_price
                    i.save()
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)
    context = {"User": User_qs, "BookOrder_list": BookOrder_qs,"Order_date": str(datetime.datetime.now()), "total_price": total_price, "Order_id": Order_id, 'SD_list': SD_qs, 'Card_list': Card_qs}
    return render(request, 'bookstore/orderPage.html', context)


def sinorderPage(request, name, Book_id):
    User_qs = User.objects.get(User_name=name)
    Book_qs = Book.objects.get(id=Book_id)
    SD_qs = ShippingDestination.objects.filter(User=User_qs).first()
    Card_qs = Card.objects.filter(User=User_qs).first()
    Order_id = Order.objects.filter(User=User_qs).last().id #홈의 오더 id
    Order_qs = Order(User=User_qs, Order_date=datetime.datetime.now(), Order_totalprice=Book_qs.Book_price)
    Order_qs.save()
    BookOrder_qs = BookOrder(Book=Book_qs, Order=Order_qs, BO_count=1, BO_price=Book_qs.Book_price)
    BookOrder_qs.save()
    BookOrder_qs = BookOrder.objects.get(Order=Order_qs)

    context = {'User': User_qs, 'sinBookOrder_list': BookOrder_qs, 'Order_id': Order_id, 'SD_list': SD_qs, 'Card_list': Card_qs}
    return render(request, 'bookstore/orderPage.html', context)


def CPorderPage(request, name, Order_id):
    User_qs = User.objects.get(User_name=name)
    Order_qs = Order.objects.get(id=Order_id)
    SD_qs = ShippingDestination.objects.filter(User=User_qs).first()
    Card_qs = Card.objects.filter(User=User_qs).first()
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)

    context = {"User": User_qs, "BookOrder_list": BookOrder_qs, "Order_date": str(datetime.datetime.now()), "total_price": Order_qs.Order_totalprice, "Order_id": Order_id, 'SD_list': SD_qs, 'Card_list': Card_qs}
    return render(request, 'bookstore/orderPage.html', context)


def orderdonePage(request, name):
    #BookSB초기화
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    for i in BookSB_qs:
        i.delete()
    context = {"User": User_qs}
    return render(request, 'bookstore/orderdonePage.html', context)


def couponselectPage(request, name, BookOrder_id):
    User_qs = User.objects.get(User_name=name)
    BookOrder_qs = BookOrder.objects.get(id=BookOrder_id)
    CP_qs = Coupon.objects.filter(User=User_qs)
    context = {"User": User_qs, 'BookOrder_list': BookOrder_qs, 'CP_list': CP_qs, 'Order_id': BookOrder_qs.Order.id}
    return render(request, 'bookstore/couponselectPage.html', context)


def CouponDCpage(request, name, BookOrder_id, coupon_id):
    User_qs = User.objects.get(User_name=name)
    BookOrder_qs = BookOrder.objects.get(id=BookOrder_id)
    CP_qs = Coupon.objects.get(id=coupon_id)

    BookOrder_qs.CP_kind = CP_qs.CP_kind    #쿠폰 이름 넣어주기
    BookOrder_qs.save()

    #할인하기전에 총값에 기존값 빼주기
    BookOrder_qs.Order.Order_totalprice += -BookOrder_qs.BO_price
    BookOrder_qs.save()

    #할인값 저장해주기
    if coupon_id == 1: #10퍼센트
        BookOrder_qs.BO_DC_price = BookOrder_qs.BO_price - (BookOrder_qs.BO_price * 0.05)
        BookOrder_qs.save()
    elif coupon_id == 2:
        BookOrder_qs.BO_DC_price = BookOrder_qs.BO_price - 1000
        BookOrder_qs.save()

    #할인적용한 총 가격 수정해주기
    BookOrder_qs.Order.Order_totalprice += BookOrder_qs.BO_DC_price
    BookOrder_qs.save()

    CP_qs = Coupon.objects.filter(User=User_qs)
    BookOrder_qs = BookOrder.objects.get(id=BookOrder_id)
    context = {"User": User_qs, 'DC_BookOrder_list': BookOrder_qs, 'CP_list': CP_qs, 'Order_id': BookOrder_qs.Order.id}
    return render(request, 'bookstore/couponselectPage.html', context)


def couponPage(request, name):
    User_qs = User.objects.get(User_name=name)
    CP_qs = Coupon.objects.filter(User=User_qs)
    context = {'User': User_qs, 'CP_list': CP_qs}

    return render(request, 'bookstore/couponPage.html', context)


def regPage(request):
    return render(request, 'bookstore/regPage.html')


def regConPage(request):
    #받아야되는데이터 User, Card, 주소, 장바구니(자동으로 데이터 추가)
    name = request.POST['name']
    id = request.POST['id']
    pw = request.POST['pw']
    re_pw = request.POST['re_pw']
    SD_num = request.POST['sd_num'] #우편번호
    SD_ba = request.POST['sd_ba'] #기본주소
    SD_da = request.POST['sd_da'] #상세주소
    card_name = request.POST['card_name']
    card_num = request.POST['card_num']
    card_date = request.POST['card_date']
    #장바구니,카드,배송지에 User추가하기

    if name != "" and id != "" and pw != "" and re_pw != "":
        if pw == re_pw:
            #유저 저장
            user_qs = User(User_name=name, User_id=id, User_pw=pw)
            user_qs.save()
            #유저배송지 저장
            sd_qs = ShippingDestination(User=User.objects.get(User_name=name), SD_num=SD_num, SD_ba=SD_ba, SD_da=SD_da)
            sd_qs.save()
            #유저카드 저장
            card_qs = Card(User=User.objects.get(User_name=name), Card_name=card_name, Card_num=card_num, Card_date=card_date)
            card_qs.save()
            #유저 장바구니 저장
            sb_qs = ShoppingBasket(User=User.objects.get(User_name=name))
            sb_qs.save()
            return HttpResponseRedirect(reverse('bookstore:login'))
        else:
            return HttpResponse('비밀번호가 일치하지 않습니다.')
    else:
        return HttpResponse("빈칸이 있습니다.")


def userinfoPage(request, name):
    if request.method == "POST":
        name = request.POST['name']
        id = request.POST['id']
        pw = request.POST['pw']
        SD_num = request.POST['sd_num'] #우편번호
        SD_ba = request.POST['sd_ba'] #기본주소
        SD_da = request.POST['sd_da'] #상세주소
        card_name = request.POST['card_name']
        card_num = request.POST['card_num']
        card_date = request.POST['card_date']
        # 유저 저장
        user_qs = User(User_name=name, User_id=id, User_pw=pw)
        user_qs.save()
        # 유저배송지 저장
        sd_qs = ShippingDestination(User=User.objects.get(User_name=name), SD_num=SD_num, SD_ba=SD_ba, SD_da=SD_da)
        sd_qs.save()
        # 유저카드 저장
        card_qs = Card(User=User.objects.get(User_name=name), Card_name=card_name, Card_num=card_num, Card_date=card_date)
        card_qs.save()
        qs_User = User.objects.get(User_name=name)
        qs_Book = Book.objects.all()
        context = {'User_list': qs_User, 'Book_list': qs_Book}
        return render(request, 'bookstore/homePage.html', context)
    else:
        User_qs = User.objects.get(User_name=name)
        SD_qs = ShippingDestination.objects.get(User=User_qs)
        Card_qs = Card.objects.get(User=User_qs)
        context = {'User_list': User_qs, 'SD_list': SD_qs, 'Card_list': Card_qs}
        return render(request, 'bookstore/userinfoPage.html', context)


def sdaddPage(request, name):
    if request.method == "POST":
        SD_num = request.POST['sd_num'] #우편번호
        SD_ba = request.POST['sd_ba'] #기본주소
        SD_da = request.POST['sd_da'] #상세주소
        # 유저배송지 저장
        sd_qs = ShippingDestination(User=User.objects.get(User_name=name), SD_num=SD_num, SD_ba=SD_ba, SD_da=SD_da)
        sd_qs.save()

    User_qs = User.objects.get(User_name=name)
    SD_qs = ShippingDestination.objects.filter(User=User_qs)
    context = {'User_list': User_qs, 'SD_list': SD_qs}
    return render(request, 'bookstore/sdaddPage.html', context)


def cardaddPage(request, name):
    if request.method == "POST":
        card_name = request.POST['card_name']
        card_num = request.POST['card_num']
        card_date = request.POST['card_date']
        # 유저카드 저장
        card_qs = Card(User=User.objects.get(User_name=name), Card_name=card_name, Card_num=card_num, Card_date=card_date)
        card_qs.save()

    User_qs = User.objects.get(User_name=name)
    Card_qs = Card.objects.filter(User=User_qs)
    context = {'User_list': User_qs, 'Card_list': Card_qs}
    return render(request, 'bookstore/cardaddPage.html', context)