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
            qs = User.objects.get(User_id=id_temp)
            if id_temp == qs.User_id and pw_temp == qs.User_pw:
                print("계정 일치")
                context = {'User_list': qs}
                return render(request, 'bookstore/loginPage.html', context)
            else:
                print("계정 불일치 try")
            return HttpResponse('계정 불일치')
        except:
            return HttpResponse('아이디 혹은 비밀번호가 존재하지 않습니다.')
    else:
        return render(request, 'bookstore/loginPage.html')


def homePage(request, name):
    qs_User = User.objects.get(User_name=name)
    qs_Book = Book.objects.all()
    context = {'User_list': qs_User, 'Book_list': qs_Book}
    return render(request, 'bookstore/homePage.html', context)


def cartPage(request, name):
    qs_User = User.objects.get(User_name=name)
    qs_Book = Book.objects.all()
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    context = {'User_list': qs_User, 'Book_list': qs_Book, 'BookSB_list': BookSB_qs}
    return render(request, 'bookstore/cartPage.html', context)


def cartaddPage(request, name, book_id):
    # 홈에서 장바구니 클릭시 이벤트
    # 책 재고량 -1
    # User 장바구니에 Book 추가됨
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    Book_qs = Book.objects.get(id=book_id)
    #책 stock -1 해주기
    Book_qs.Book_stock += -1
    Book_qs.save()
    #유저장바구니리스트에 책,장바구니 추가
    BookSB_qs = BookSB(ShoppingBasket=SB_qs, Book=Book_qs)
    BookSB_qs.save()
    #name에 해당하는 유저 장바구니 리스트 가져오기
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    context = {'User_list': User_qs, 'BookSB_list': BookSB_qs}
    return render(request, 'bookstore/cartPage.html', context)


def cartdelPage(request, name, book_id):
    #장바구니 페이지에서 장바구니 지우기 클릭시 이벤트
    #책 재고량 +1
    #User 장바구니에 Book 제거
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    Book_qs = Book.objects.get(id=book_id)
    # 책 stock +1 해주기
    Book_qs.Book_stock += 1
    Book_qs.save()
    #유저장바구니리스트에 책,장바구니 지우기
    BookSB_qs = BookSB.objects.filter(Book=Book_qs)
    BookSB_qs.last().delete()  #지워주기
    #
    User_qs = User.objects.get(User_name=name)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    context = {'User_list': User.objects.get(User_name=name), 'Book_list': Book.objects.all(), "BookSB_list": BookSB_qs}
    return render(request, 'bookstore/cartPage.html', context)

def orderConPage(request, name, book_id):   #주문 페이지 들어가기전에 쿼리 생성 및 저장
    try:

        #개인장바구니에 넣어서 구매하도록하자
        User_qs = User.objects.get(User_name=name)
        Card_qs = Card.objects.filter(User=User_qs).first() #카드 첫번째
        SD_qs = ShippingDestination.objects.filter(User=User_qs).first() #집 첫번째
        Book_qs = Book.objects.get(id=book_id)
        SB_qs = ShoppingBasket.objects.get(User=User_qs)
        #장바구니에 책 넣기
        BookSB_qs = BookSB(Book=Book_qs, ShoppingBasket=SB_qs)
        BookSB_qs.save()
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
        #주문 총액 저장
        order_totalAmount = 0
        for i in BookSB_qs:
            order_totalAmount += i.Book.Book_price
        #Order 쿼리 저장
        Order_qs = Order(User=User_qs, Order_date=datetime.datetime.now(), Order_count=len(BookSB_qs), Order_price=order_totalAmount, Card_name=Card_qs.Card_name, Card_num=Card_qs.Card_num, Card_date=Card_qs.Card_date)
        Order_qs.save()
        order_id = Order_qs.id
        #BookOrder 쿼리 저장
        BookOrder_qs = BookOrder(Book=Book_qs, Order=Order_qs)
        BookOrder_qs.save()
        #리턴
        BookOrder_qs = BookOrder.objects.filter(Order=Order.objects.get(id=order_id))
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
        print('BookOrder_list :', BookOrder_qs)
        print("BookSB_list :", BookSB_qs)
        context = {'BookOrder_list': BookOrder_qs, 'BookSB_list': BookSB_qs, 'SD_list': SD_qs}
        return render(request, 'bookstore/orderConPage.html', context)
    except:
        BookOrder_qs = BookOrder.objects.filter(Order=Order.objects.get)
#수정해야됨
def orderPage(request, BookOrder_id):
    BookOrder_qs = BookOrder.objects.get(id=BookOrder_id)
    context = {'BookOrder_list': BookOrder_qs}
    return render(request, 'bookstore/orderPage.html', context)


def couponselectPage(request, name, BookOrder_id, BookSB_id):
    print("쿠폰선택페이지")


def couponselectPage(request, BookOrder_id):
    BookOrder_qs = BookOrder.objects.get(id=BookOrder_id)
    #쿠폰 선택 후 선택 html 반환
    #쿠폰 취소 추가
    #쿠폰 취소시 기존 orderpage로 이동
    context = {'BookOrder_list': BookOrder_qs}
    return render(request, 'bookstore/couponselectPage.html', context)

def couponPage(request, name):
    User_qs = User.objects.get(User_name=name)
    CP_qs = Coupon.objects.filter(User=User_qs)
    context = {'User_list': User_qs, 'CP_list': CP_qs}

    return render(request, 'bookstore/couponPage.html', context)


#수정해야됨
def orderdonePage(request, name):
    #책 -1해줘야됨
    print("주문완료 페이지")
    User_qs = User.objects.get(User_name=name)
    context = {'User_list': User_qs}
    return render(request, 'bookstore/orderdonePage.html', context)


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