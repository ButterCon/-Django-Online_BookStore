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
    context = {'User': User_qs, 'Book_list': Book_qs}
    return render(request, 'bookstore/homePage.html', context)


def cartPage(request, name):
    User_qs = User.objects.get(User_name=name)
    #Order_qs id로 넣어야됨
    Order_qs = Order.objects.filter(User=User_qs).last()    #마지막 장바구니
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)
    context = {'User': User_qs, 'Order_list': Order_qs, 'BookOrder_list': BookOrder_qs}
    return render(request, 'bookstore/cartPage.html', context)


def cartaddPage(request, name, book_id):
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
    #BookOrder 책 개수 저장하기
    Book_stock = len(BookSB.objects.filter(Book=Book_qs))   #넘어온 책이 저장된 개수를 저장
    #BookOrder 책 가격 넣기
    Book_price_add = 0
    for i in BookSB.objects.filter(Book=Book_qs):   #넘어온 책이 저장된 가격를 저장
        Book_price_add += i.Book.Book_price
    #Order -> 주문 총액 저장
    order_totalAmount = 0
    for i in BookSB_qs:
        order_totalAmount += i.Book.Book_price
    #Order 쿼리 저장
    if len(BookSB.objects.filter(ShoppingBasket=SB_qs))==1:   #처음 저장할 때, 주문을 만들어준다, 주문 진행 할 때는 이걸로 계속 진행함
        Order_qs = Order(User=User_qs, Order_date=datetime.datetime.now(), Order_totalprice=order_totalAmount)
        Order_qs.save()
    else:   #주문리스트에 저장돼 있을경우 데이터 업데이트해준다.
        Order_qs = Order.objects.filter(User=User_qs).last()    #최신 주문가져오기
        Order_qs.Order_totalprice = order_totalAmount   #금액 업데이트해준다, 혹시 나중에 금액 빼거나 추가할 때 업데이트 or 추가 중에 뭐가 더 좋을지 선택
    Order_qs.save()
    order_id = Order_qs.id  #주문번호
    #BookOrder 쿼리 저장
    if Book_stock == 1: #책주문리스트에 처음 책을 저장할 때, 책의개수가 1일 때, 새로운 쿼리를 생성해준다.
        BookOrder_qs = BookOrder(Book=Book_qs, Order=Order_qs, BO_count=Book_stock, BO_price=Book_price_add)
        BookOrder_qs.save()
    else:   #책주문리스트에 기존에 책이 있을경우, 책 수량 +1, 책 가격 +
        BookOrder_qs = BookOrder.objects.filter(Book=Book_qs)   #책 쿼리 찾아서 데이터 넣어줘야됨
        BookOrder_qs.BO_count += 1  #책 수량 추가
        BookOrder_qs.BO_price += Book_qs.Book_price #책 가격을 한번더 더해준다.
        BookOrder_qs.save() #쿼리 저장
    #####################쿠폰 어떡할거야?#######################
    #models에 BO_DC_price를 전체 할인가로 할것인가, 한개의 할인가로 할것인가
    #orderPage.html 19번줄 수정해줘야됨
    #리턴
    BookOrder_qs = BookOrder.objects.filter(Order=Order.objects.get(id=order_id))   #주문번호에 해당하는 책주문리스트 가져온다.
    context = {'User': User_qs, 'BookOrder_list': BookOrder_qs} #책주문리스트에 저장된값들: 책 수량, 책 가격
    return render(request, 'bookstore/cartPage.html', context)


def cartdelPage(request, name,Order_id ,book_id):
    #장바구니 페이지에서 장바구니 지우기 클릭시 이벤트
    #책 재고량 +1
    #User 장바구니에 Book 제거
    User_qs = User.objects.get(User_name=name)
    Book_qs = Book.objects.get(id=book_id)  #지워야하는 책 쿼리 가져옴
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    Order_qs = Order.objects.get(id=Order_id)   #현재 진행중인 카트id가져오기
    # 책 stock +1 해주기
    Book_qs.Book_stock += 1
    Book_qs.save()
    #유저장바구니리스트(BookSB)에 책 빼주기 -1
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, Book=Book_qs) #장바구니에서 지워줄 책리스트 가져오기
    BookSB_qs.first().delect()  #장바구니에 책 지워줌
    #책주문내역리스트(BookOrder)에 책 빼주기 -1
    #BookOrder에 책가격 뺴주기
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs, Book=Book_qs) #책주문내역에 가져옴 책
    if BookOrder_qs.BO_count == 1:  #책이 하나만 들어있을 경우
        BookOrder_qs.delete()
    elif BookOrder_qs.BO_count > 1: #책이 하나이상 들어있을 경우
        BookOrder_qs.BO_count += -1
        BookOrder_qs.BO_price += -Book_qs.Book_price    #책가격 뺴주기
        Order_qs.Order_totalprice += -Book_qs.Book_price
        Order_qs.save()
        BookOrder_qs.save()
    #유저장바구니리스트에 책,장바구니 지우기
    context = {'User': User_qs, "BookOrder_list": BookOrder_qs}
    return render(request, 'bookstore/cartPage.html', context)

def orderConPage(request, name, book_id):   #주문 페이지 들어가기전에 쿼리 생성 및 저장
    #개인장바구니에 넣어서 구매하도록하자
    User_qs = User.objects.get(User_name=name)
    Card_qs = Card.objects.filter(User=User_qs).first() #카드 첫번째
    SD_qs = ShippingDestination.objects.filter(User=User_qs).first() #집 첫번째
    Book_qs = Book.objects.get(id=book_id)
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    #장바구니에 책 넣기
    BookSB(Book=Book_qs, ShoppingBasket=SB_qs).save()
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs)
    #BookOrder 책 개수 저장하기
    Book_stock = len(BookSB.objects.filter(Book=Book_qs))   #넘어온 책이 저장된 개수를 저장
    #BookOrder 책 가격 넣기
    Book_price_add = 0
    for i in BookSB.objects.filter(Book=Book_qs):   #넘어온 책이 저장된 가격를 저장
        Book_price_add += i.Book.Book_price
    #Order -> 주문 총액 저장
    order_totalAmount = 0
    for i in BookSB_qs:
        order_totalAmount += i.Book.Book_price
    #Order 쿼리 저장
    if len(BookSB.objects.filter(ShoppingBasket=SB_qs))==1:   #처음 저장할 때, 주문을 만들어준다, 주문 진행 할 때는 이걸로 계속 진행함
        Order_qs = Order(User=User_qs, Order_date=datetime.datetime.now(), Order_totalprice=order_totalAmount)
        Order_qs.save()
    else:   #주문리스트에 저장돼 있을경우 데이터 업데이트해준다.
        Order_qs = Order.objects.filter(User=User_qs).last()    #최신 주문가져오기
        Order_qs.Order_totalprice = order_totalAmount   #금액 업데이트해준다, 혹시 나중에 금액 빼거나 추가할 때 업데이트 or 추가 중에 뭐가 더 좋을지 선택
    Order_qs.save()
    order_id = Order_qs.id  #주문번호
    #BookOrder 쿼리 저장
    if Book_stock == 1: #책주문리스트에 처음 책을 저장할 때, 책의개수가 1일 때, 새로운 쿼리를 생성해준다.
        BookOrder_qs = BookOrder(Book=Book_qs, Order=Order_qs, BO_count=Book_stock, BO_price=Book_price_add)
        BookOrder_qs.save()
    else:   #책주문리스트에 기존에 책이 있을경우, 책 수량 +1, 책 가격 +
        BookOrder_qs = BookOrder.objects.filter(Book=Book_qs)   #책 쿼리 찾아서 데이터 넣어줘야됨
        BookOrder_qs.BO_count += 1  #책 수량 추가
        BookOrder_qs.BO_price += Book_qs.Book_price #책 가격을 한번더 더해준다.
        BookOrder_qs.save() #쿼리 저장
    #####################쿠폰 어떡할거야?#######################
    #models에 BO_DC_price를 전체 할인가로 할것인가, 한개의 할인가로 할것인가
    #orderPage.html 19번줄 수정해줘야됨
    #리턴
    BookOrder_qs = BookOrder.objects.filter(Order=Order.objects.get(id=order_id))   #주문번호에 해당하는 책주문리스트 가져온다.
    context = {'User': User_qs, 'BookOrder_list': BookOrder_qs, 'SD': SD_qs, 'CD': Card_qs} #책주문리스트에 저장된값들: 책 수량, 책 가격
    return render(request, 'bookstore/orderPage.html', context)


#수정해야됨, cartPage.html 12번줄 구매하기 수정해주기, 전달값 수정, 이름만 가면 안됨
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
    #책 장바구니 초기화 해야됨
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