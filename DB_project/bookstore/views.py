from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from .models import User
from .models import ShippingDestination
from .models import ShoppingBasket
from .models import Card
from .models import Order
from .models import Book
from .models import BookSB
from .models import BookOrder
from .models import Coupon
from .models import DongseoPay
import datetime

# Create your views here.
def test1(request):
    request.session['User'] = '진현우'
    return render(request, "bookstore/test1.html")


def test2(request):
    User_name = request.session['User']
    context = {"User": User_name}
    return render(request, "bookstore/test2.html", context)


def regPage(request):
    if request.method == "POST":    #값을 받을경우 실행
        if request.POST['name'] != "" and request.POST['id'] != "" and request.POST['pw'] != "" and request.POST['re_pw'] != "" and request.POST['sd_num'] != "" and request.POST['sd_ba'] != "" and request.POST['sd_da'] != "" and request.POST['card_name'] != "" and request.POST['card_num'] != "" and request.POST['card_date'] != "":
            if request.POST['pw'] == request.POST['re_pw']: #비밀번호가 같을경우
                if len(User.objects.filter(User_id=request.POST['id'])) == 0:   #존재하는 아이디일경우
                    User_qs = User(User_id=request.POST['id'],
                                   User_pw=request.POST['pw'],
                                   User_name=request.POST['name'])
                    User_qs.save()
                    SD_qs = ShippingDestination(User=User_qs,
                                                SD_num=request.POST['sd_num'],
                                                SD_ba=request.POST['sd_ba'],
                                                SD_da=request.POST['sd_da'])
                    SD_qs.save()
                    Card_qs = Card(User=User_qs,
                                   Card_name=request.POST['card_name'],
                                   Card_num=request.POST['card_num'],
                                   Card_date=request.POST['card_date'])
                    Card_qs.save()
                    ShoppingBasket(User=User_qs).save()
                    Coupon(User=User_qs,
                           CP_kind="10퍼센트").save()
                    Coupon(User=User_qs,
                           CP_kind="1000원").save()
                    User_qs.Select_SD_id = SD_qs.id
                    User_qs.Select_Card_id = Card_qs.id
                    User_qs.save()
                    return HttpResponseRedirect(reverse('bookstore:login'))
                else:
                    context = {"mes": "존재하는 아이디입니다."}
                    return render(request, "bookstore/REGPage.html", context)
            else:
                context = {"mes": "아이디 혹은 비밀번호가 일치하지 않습니다."}
                return render(request, "bookstore/REGPage.html", context)
        else:
            context = {"mes": "빈칸이 있습니다."}
            return render(request, "bookstore/REGPage.html", context)
    else:
        return render(request, 'bookstore/REGPage.html')


def login(request):
    if request.method == "POST":
        post_id = request.POST['id']
        post_pw = request.POST['pw']
        if post_id != "" and post_pw != "":
            if len(User.objects.filter(User_id=post_id)) != 0:
                if post_id == get_object_or_404(User, User_id=post_id).User_id and \
                        post_pw == get_object_or_404(User, User_id=post_id).User_pw:
                    #세션 전달
                    User_qs = get_object_or_404(User, User_id=post_id)
                    print("여기")
                    request.session['User_id'] = User_qs.id
                    return HttpResponseRedirect(reverse('bookstore:home', args=[User_qs.id]))
                else:
                    return render(request, 'bookstore/loginPage.html', {'mes': '아이디 혹은 비밀번호가 일치하지 않습니다.'})
            else:
                return render(request, "bookstore/loginPage.html", {"mes": "계정이 존재하지 않습니다."})
        else:
            return render(request, "bookstore/loginPage.html", {"mes": "빈칸이 있습니다."})
    elif request.method == "GET":
        return render(request, 'bookstore/loginPage.html')


def logout(request):
    try:
        del request.session['User_id']
    except KeyError:
        pass
    return render(request, "bookstore/loginPage.html", {"mes": "로그아웃 되었습니다."})


def homePage(request, User_id):
    #장바구니 지워주기
    User_qs = get_object_or_404(User, id=User_id)
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
    try:
        del request.session['Order_id']
    except KeyError:
        pass
    Order_qs = Order.objects.filter(User=User_qs, Order_con=0)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=0)
    CP_qs = Coupon.objects.filter(User=User_qs, CP_state=1) #사용대기쿠폰가져옴
    if BookSB_qs is not None:
        for i in BookSB_qs:
            i.Book.Book_stock += 1
            i.Book.save()
            i.delete()
    if Order_qs is not None:
        for i in Order_qs:
            i.delete()
    if CP_qs is not None:
        for i in CP_qs:
            i.CP_state = 0  #사용대기 -> 미사용
            i.save()
    Book_qs = Book.objects.all()

    #세션 전달
    Order_qs = Order(User=User_qs)
    Order_qs.save()
    request.session["Order_id"] = Order_qs.id

    context = {'User': User_qs,
               'Book_list': Book_qs}
    return render(request, 'bookstore/homePage.html', context)


def cartPage(request):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=1)
    #총가격
    Book_total_price = 0
    for i in BookSB_qs:
        Book_total_price += i.Book.Book_price
    context = {'User': User_qs,
               'BookSB_list': BookSB_qs,
               'Book_total_price': Book_total_price}
    return render(request, 'bookstore/CARTPage.html', context)


def sincartaddPage(request, book_id):
    # 홈에서 장바구니 클릭시 이벤트
    # 책 재고량 -1
    # 책 재고량 수정하고 나머지는 orderCon이라 같음
    # User 장바구니에 Book 추가됨
    User_qs = get_object_or_404(User, id=request.session['User_id'])
    Book_qs = get_object_or_404(Book, id=book_id)
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
    #책 stock -1 해주기
    Book_qs.Book_stock += -1
    Book_qs.save()
    #장바구니에 책 넣기
    BookSB(Book=Book_qs, ShoppingBasket=SB_qs, BookSB_type=0).save()

    return HttpResponseRedirect(reverse("bookstore:order"))


def mulcartaddPage(request, book_id):
    # 홈에서 장바구니 클릭시 이벤트
    # 책 재고량 -1
    # 책 재고량 수정하고 나머지는 orderCon이라 같음
    # User 장바구니에 Book 추가됨
    User_qs = get_object_or_404(User, id=request.session['User_id'])
    Book_qs = get_object_or_404(Book, id=book_id)
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
    #책 stock -1 해주기
    Book_qs.Book_stock += -1
    Book_qs.save()
    #장바구니에 책 넣기
    BookSB(Book=Book_qs, ShoppingBasket=SB_qs).save()
    BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs) #장바구니 가져오기
    #총가격
    Book_total_price = 0
    for i in BookSB_qs:
        Book_total_price += i.Book.Book_price

    context = {'User': User_qs,
               'BookSB_list': BookSB_qs,
               'Book_total_price': Book_total_price}
    return render(request, 'bookstore/CARTPage.html', context)


def cartdelPage(request, book_id):
    #장바구니 페이지에서 장바구니 지우기 클릭시 이벤트
    #책 재고량 +1
    #User 장바구니에 Book 제거
    User_qs = get_object_or_404(User, id=request.session['User_id'])
    Book_qs = get_object_or_404(Book, id=book_id)  #지워야하는 책 쿼리 가져옴
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
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
    context = {'User': User_qs,
               "BookSB_list": BookSB_qs,
               'Book_total_price': total}
    return render(request, 'bookstore/CARTPage.html', context)


def orderPage(request):
    #작동방식
    #BookOrder.CP_kind = ""일경우 쿠폰 가격 출력안함
    if len(BookOrder.objects.filter(Order=get_object_or_404(Order, id=request.session["Order_id"]))) != 0:
        #이미 BookOrder쿼리가 존재할 경우, 기존 데이터 뿌려준다.
        User_qs = get_object_or_404(User, id=request.session['User_id'])
        Order_qs = get_object_or_404(Order, id=request.session["Order_id"])
        BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)

        page = 'OrderlistPage'
        context = {"User": User_qs,
                   "Order_list": Order_qs,
                   "BookOrder_list": BookOrder_qs,
                   'Page': page}

        return render(request, 'bookstore/ORDERPage.html', context)

    User_qs = get_object_or_404(User, id=request.session['User_id'])
    SB_qs = get_object_or_404(ShoppingBasket, User=User_qs)
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])

    if len(BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=0)) != 0:    #해당유저의 장바구니에 바로구매목록이 있으면 바로구매로 진행함
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=0)
        print("바로구매")
    else:
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=1)
        print("장바구니구매")
    total_price = 0 #총 금액

    #처음 장바구니리스트를 주문에 넣어줌
    for i in BookSB_qs:
        total_price += i.Book.Book_price  #모든 책 가격 더하기
        qs = BookOrder(Book=i.Book, Order=Order_qs, BO_count=1, BO_price=i.Book.Book_price)
        qs.save()

    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)
    for i in BookOrder_qs:
        if i.id == None:
            continue
        for j in BookOrder_qs:
            if j.id == None:
                continue
            if i.id != j.id:    #같은 주문리스트면 패스
                if i.Book.id == j.Book.id:  #같은 책일경우
                    j.delete()  #중복되는 책 하나 제거
                    i.BO_count += 1 #책 개수 +1
                    i.BO_price += i.Book.Book_price #책 값 한번더 더해줌
                    i.save()    #저장

    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)

    Order_qs.Order_totalprice = total_price
    #Order_qs.Order_DC_totalprice = Order_qs.Order_totalprice
    Order_qs.save()

    page = 'OrderlistPage'
    context = {"User": User_qs,
               "Order_list": Order_qs,
               "BookOrder_list": BookOrder_qs,
               'Page': page}

    return render(request, 'bookstore/ORDERPage.html', context)


def orderPaymentPage(request):
    # 결제 뷰,
    # 결제 후 주문 완료로
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])
    SD_qs = get_object_or_404(ShippingDestination, id=User_qs.Select_SD_id)
    Card_qs = get_object_or_404(Card, id=User_qs.Select_Card_id)
    DP_qs = get_object_or_404(DongseoPay, User=User_qs)
    if request.method == "POST":
        if int(request.POST["DP_UsedPrice"]) > DP_qs.DP_price:
            page = "PaymentPage"
            mes = "사용금액이 잔액을 초과합니다."
            context = {"User": User_qs,
                       "SD_list": SD_qs,
                       "Card_list": Card_qs,
                       "Order_list": Order_qs,
                       "DP_list": DP_qs,
                       "mes": mes,
                       "Page": page}

            return render(request, 'bookstore/ORDERPage.html', context)

        else:
            if Order_qs.Order_DC_totalprice != 0:   #할인 한경우
                if Order_qs.Order_DC_totalprice < int(request.POST["DP_UsedPrice"]):
                    #할인 값보다 사용금액이 클경우
                    page = "PaymentPage"
                    mes = "사용금액이 총액을 초과합니다."
                    context = {"User": User_qs,
                               "SD_list": SD_qs,
                               "Card_list": Card_qs,
                               "Order_list": Order_qs,
                               "DP_list": DP_qs,
                               "mes": mes,
                               "Page": page}

                    return render(request, 'bookstore/ORDERPage.html', context)

                Order_qs.Order_DP = Order_qs.Order_DC_totalprice - int(request.POST["DP_UsedPrice"])
            elif Order_qs.Order_DC_totalprice == 0: #할인 안한경우
                if Order_qs.Order_totalprice < int(request.POST["DP_UsedPrice"]):
                    #할인 값보다 사용금액이 클경우
                    page = "PaymentPage"
                    mes = "사용금액이 총액을 초과합니다."
                    context = {"User": User_qs,
                               "SD_list": SD_qs,
                               "Card_list": Card_qs,
                               "Order_list": Order_qs,
                               "DP_list": DP_qs,
                               "mes": mes,
                               "Page": page}

                    return render(request, 'bookstore/ORDERPage.html', context)

                Order_qs.Order_DP = Order_qs.Order_totalprice - int(request.POST["DP_UsedPrice"])
            Order_qs.save()

            DP_qs.DP_UsedPrice = int(request.POST["DP_UsedPrice"])
            DP_qs.DP_price -= int(request.POST["DP_UsedPrice"])
            DP_qs.DP_history = Order_qs.id
            DP_qs.save()

            page = "PaymentPage"
            context = {"User": User_qs,
                       "SD_list": SD_qs,
                       "Card_list": Card_qs,
                       "Order_list": Order_qs,
                       "DP_list": DP_qs,
                       "Page": page}

            return render(request, 'bookstore/ORDERPage.html', context)

    elif request.method == "GET":
        Order_qs.Order_date = datetime.datetime.now()
        Order_qs.save()
        page = "PaymentPage"
        context = {"User": User_qs,
                   "SD_list": SD_qs,
                   "Card_list": Card_qs,
                   "Order_list": Order_qs,
                   "DP_list": DP_qs,
                   "Page": page}

        return render(request, 'bookstore/ORDERPage.html', context)
#수정중

def CPorderPage(request):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)

    page = 'OrderlistPage'
    context = {"User": User_qs,
               "Order_list": Order_qs,
               "BookOrder_list": BookOrder_qs,
               'Page': page}

    return render(request, 'bookstore/ORDERPage.html', context)


def orderdonePage(request):
    #BookSB초기화
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    SB_qs = ShoppingBasket.objects.get(User=User_qs)
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])

    if len(BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=0)) != 0:  # 해당유저의 장바구니에 바로구매목록이 있으면 바로구매로 진행함
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=0)
        print("바로구매완료")
    else:
        BookSB_qs = BookSB.objects.filter(ShoppingBasket=SB_qs, BookSB_type=1)
        print("장바구니구매완료")

    for i in BookSB_qs:
        i.delete()
    #사용된 쿠폰 CP_state = 2로 바꿔주기
    BookOrder_qs = BookOrder.objects.filter(Order=Order_qs)
    for i in BookOrder_qs:
        if i.CP_kind != "":
            CP_qs = get_object_or_404(Coupon, CP_kind=i.CP_kind)
            CP_qs.CP_state = 2
            CP_qs.save()
    #Order_con = 1로 바꿔주기, 세션에서 삭제
    Order_qs.Order_con = 1
    Order_qs.save()
    del request.session["Order_id"]

    page = 'OrderDonePage'
    context = {"User": User_qs,
               "BookOrder_list": BookOrder_qs,
               'Page': page}
    return render(request, 'bookstore/ORDERPage.html', context)


def couponselectPage(request, BookOrder_id):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    BookOrder_qs = get_object_or_404(BookOrder, id=BookOrder_id)    #할인적용할 주문책리스트
    CP_qs = Coupon.objects.filter(User=User_qs).exclude(CP_state=2)

    context = {"User": User_qs,
               'BookOrder_list': BookOrder_qs,
               'CP_list': CP_qs}
    return render(request, 'bookstore/CPselectPage.html', context)


def CouponDCpage(request, BookOrder_id, CP_id):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])
    BookOrder_qs = get_object_or_404(BookOrder, id=BookOrder_id)
    CP_qs = get_object_or_404(Coupon, id=CP_id)

    if BookOrder_qs.CP_kind != "":  #현재 주문항목에 쿠폰이 적용된 경우 쿠폰을 초기화 해준다.
        qs = get_object_or_404(Coupon, CP_kind=BookOrder_qs.CP_kind)
        qs.CP_state = 0     #쿠폰 상태를 0으로 바꿔준다.
        qs.save()

    CP_qs.CP_state = 1  #선택된 쿠폰 사용처리
    CP_qs.save()

    # 쿠폰 이름 넣어주기
    BookOrder_qs.CP_kind = CP_qs.CP_kind

    #할인값 저장해주기
    if CP_id == 1: #10퍼센트
        BookOrder_qs.BO_DC_price = BookOrder_qs.BO_price - (BookOrder_qs.BO_price * 0.05)
        BookOrder_qs.save()
    elif CP_id == 2: #1000원
        BookOrder_qs.BO_DC_price = BookOrder_qs.BO_price - 1000
        BookOrder_qs.save()

    #BO_DC_price저장하기
    Order_qs.Order_DC_totalprice = 0

    for i in BookOrder.objects.filter(Order=Order_qs):
        if i.BO_DC_price != 0:  #쿠폰사용한 경우
            Order_qs.Order_DC_totalprice += i.BO_DC_price
        elif i.BO_DC_price == 0:    #쿠폰사용안한 경우
            Order_qs.Order_DC_totalprice += i.BO_price
    Order_qs.save()

    #사용한쿠폰 제외하고 가져옴
    CP_qs = Coupon.objects.filter(User=User_qs).exclude(CP_state=2)

    context = {"User": User_qs,
               'BookOrder_list': BookOrder_qs,
               'CP_list': CP_qs}
    return render(request, 'bookstore/CPselectPage.html', context)


def cpcancelPage(request, BookOrder_id, CP_id):
    #작동방식 / 쿠폰 취소하는 경우
    # Coupon.CP_state = 0
    # BookOrder.BO_DC_price = BookOrder.BO_price
    # BookOrder.CP_kind = "" , 초기화해주기
    # Order.Order_DC_totalprice 초기화
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    Order_qs = get_object_or_404(Order, id=request.session["Order_id"])
    BookOrder_qs = get_object_or_404(BookOrder, id=BookOrder_id)
    CP_qs = get_object_or_404(Coupon, id=CP_id)

    if BookOrder_qs.CP_kind != CP_qs.CP_kind:
        CP_qs = Coupon.objects.filter(User=User_qs).exclude(CP_state=2)
        context = {"User": User_qs,
                   'BookOrder_list': BookOrder_qs,
                   'CP_list': CP_qs,
                   'mes': "다른책에 사용중인 쿠폰입니다."}
        return render(request, 'bookstore/CPselectPage.html', context)
    CP_qs.CP_state = 0
    CP_qs.save()

    BookOrder_qs.BO_DC_price = 0
    BookOrder_qs.CP_kind = ""
    BookOrder_qs.save()

    Order_qs.Order_DC_totalprice = 0
    Order_qs.save()

    CP_qs = Coupon.objects.filter(User=User_qs).exclude(CP_state=2)

    context = {"User": User_qs,
               'BookOrder_list': BookOrder_qs,
               'CP_list': CP_qs}
    return render(request, 'bookstore/CPselectPage.html', context)


def couponPage(request):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    CP_qs = Coupon.objects.filter(User=User_qs, CP_state=0)  #사용안한 쿠폰 가져온다
    context = {'User': User_qs,
               'CP_list': CP_qs}

    return render(request, 'bookstore/CPPage.html', context)


def User_info(request):
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    Card_qs = Card.objects.filter(User=User_qs)
    SD_qs = ShippingDestination.objects.filter(User=User_qs)

    if request.method == "POST":
        name = request.POST['name']
        id = request.POST['id']
        pw = request.POST['pw']
        # 유저 저장
        User_qs.User_name = name
        User_qs.User_id = id
        User_qs.User_pw = pw
        User_qs.save()

        page = "InfoPage"
        context = {"User": User_qs,
                   "Card_list": Card_qs,
                   "SD_list": SD_qs,
                   "Page": page}

        return render(request, 'bookstore/USERinfoPage.html', context)

    elif request.method == "GET":
        page = "InfoPage"
        context = {"User": User_qs,
                   "Card_list": Card_qs,
                   "SD_list": SD_qs,
                   "Page": page}

        return render(request, 'bookstore/USERinfoPage.html', context)


def SD_info(request):
    User_qs = get_object_or_404(User, id=request.session['User_id'])

    if request.method == "POST":
        #빈칸이 없는경우
        if request.POST['sd_num'] != "" and request.POST['sd_ba'] != "" and request.POST['sd_da'] != "":
            SD_num = request.POST['sd_num'] #우편번호
            SD_ba = request.POST['sd_ba'] #기본주소
            SD_da = request.POST['sd_da'] #상세주소
            # 유저신규배송지 저장
            ShippingDestination(User=User_qs,
                                SD_num=SD_num,
                                SD_ba=SD_ba,
                                SD_da=SD_da).save()

            SD_qs = ShippingDestination.objects.filter(User=User_qs)
            mes = "배송지 추가가 완료되었습니다."
            page = "SDPage"
            context = {"User": User_qs,
                       "SD_list": SD_qs,
                       "Page": page,
                       "mes": mes}

            return render(request, 'bookstore/USERinfoPage.html', context)
        #빈칸이 있는경우
        else:
            SD_qs = ShippingDestination.objects.filter(User=User_qs)
            mes = "빈칸이 있습니다."
            page = "SDPage"
            context = {"User": User_qs,
                       "SD_list": SD_qs,
                       "Page": page,
                       "mes": mes}

            return render(request, 'bookstore/USERinfoPage.html', context)

    elif request.method == "GET":
        SD_qs = ShippingDestination.objects.filter(User=User_qs)

        page = "SDPage"
        context = {'User': User_qs,
                   'Page': page,
                   'SD_list': SD_qs}

        return render(request, 'bookstore/USERinfoPage.html', context)


def SD_add(request, SD_id):
    User_qs = get_object_or_404(User, id=request.session['User_id'])
    User_qs.Select_SD_id = SD_id
    User_qs.save()

    SD_qs = ShippingDestination.objects.filter(User=User_qs)
    mes = "기본배송지 선택이 완료되었습니다."
    page = "SDPage"
    context = {"User": User_qs,
               "SD_list": SD_qs,
               "Page": page,
               "mes": mes}

    return render(request, 'bookstore/USERinfoPage.html', context)


def CARD_info(request):
    User_qs = get_object_or_404(User, id=request.session["User_id"])

    if request.method == "POST":
        #빈칸이 없는경우
        if request.POST['card_name'] != "" and request.POST['card_num'] != "" and request.POST['card_date'] != "":
            card_name = request.POST['card_name']
            card_num = request.POST['card_num']
            card_date = request.POST['card_date']
            # 유저 신규카드 저장
            Card(User=User_qs,
                 Card_name=card_name,
                 Card_num=card_num,
                 Card_date=card_date).save()

            Card_qs = Card.objects.filter(User=User_qs)
            mes = "카드 추가가 완료되었습니다."
            page = "CardPage"
            context = {"User": User_qs,
                       'Card_list': Card_qs,
                       "Page": page,
                       "mes": mes}

            return render(request, 'bookstore/USERinfoPage.html', context)
        #빈칸이 있는경우
        else:
            Card_qs = Card.objects.filter(User=User_qs)
            mes = "빈칸이 있습니다."
            page = "CardPage"
            context = {"User": User_qs,
                       "Card_list": Card_qs,
                       "Page": page,
                       "mes": mes}

            return render(request, 'bookstore/USERinfoPage.html', context)

    elif request.method == "GET":
        Card_qs = Card.objects.filter(User=User_qs)

        page = "CardPage"
        context = {'User': User_qs,
                   'Page': page,
                   'Card_list': Card_qs}

        return render(request, 'bookstore/USERinfoPage.html', context)


def CARD_add(request, CARD_id):
    User_qs = get_object_or_404(User, id=request.session['User_id'])
    User_qs.Select_Card_id = CARD_id
    User_qs.save()

    Card_qs = Card.objects.filter(User=User_qs)
    mes = "카드 추가가 완료되었습니다."
    page = "CardPage"
    context = {"User": User_qs,
               "Card_list": Card_qs,
               "Page": page,
               "mes": mes}

    return render(request, 'bookstore/USERinfoPage.html', context)


def DP_ref(request):
    try:
        User_qs = get_object_or_404(User, id=request.session["User_id"])
        if len(DongseoPay.objects.filter(User=User_qs)) == 0:
            # 유저에 동서페이가 발급안된경우
            mes = '동서페이 미발급'
            page = 'EnrollPage'
            context = {"User": User_qs,
                       "Page": page,
                       "mes": mes}
            return render(request, "bookstore/DP.html", context)
        else:
            # 페이 발급되어 있는경우
            DP_qs = get_object_or_404(DongseoPay, User=User_qs)

            page = 'ReferencePage'
            context = {"User": User_qs,
                       "DP_list": DP_qs,
                       "Page": page}
        return render(request, 'bookstore/DP.html', context)
    except KeyError:
        pass
    mes = "세션이 만료되었습니다. 다시로그인해주세요."
    return HttpResponseRedirect(reverse('bookstore:login'), args=[mes])


def DP_issue(request):
    #DP등록
    User_qs = get_object_or_404(User, id= request.session["User_id"])
    DP_qs = DongseoPay(User=User_qs) #DP 생성
    DP_qs.save()

    page = 'ReferencePage'
    mes = "동서페이가 발급되었습니다"
    context = {"User": User_qs,
               "DP_list": DP_qs,
               "Page": page,
               "mes": mes}
    return render(request, "bookstore/DP.html", context)


def DP_charege(request):
    #DP충전
    User_qs = get_object_or_404(User, id= request.session["User_id"])
    DP_qs = get_object_or_404(DongseoPay, User=User_qs)

    if request.method == "POST":
        #최근에 충전된 금액 넣어주기기
        DP_qs.DP_ChargePrice = int(request.POST["DP_ChargePrice"])
        #기존금액이랑 충전액 더해주기
        DP_qs.DP_price += int(request.POST["DP_ChargePrice"])
        DP_qs.save()

        page = "ReferencePage"
        mes = "동서페이가 충전되었습니다."
        context = {"User": User_qs,
                   "DP_list": DP_qs,
                   "Page": page,
                   "mes": mes}
        return render(request, "bookstore/DP.html", context)

    elif request.method == "GET":
        page = 'ChargePage'
        context = {"User": User_qs, "Page": page}
        return render(request, "bookstore/DP.html", context)


def DP_del(request):
    #DP해지
    User_qs = get_object_or_404(User, id=request.session["User_id"])
    DP_qs = get_object_or_404(DongseoPay, User=User_qs)
    DP_qs.delete()

    page = 'InfoPage'
    mes = "동서페이가 해지되었습니다."
    context = {"User": User_qs,
               "Page": page,
               "mes": mes}
    return render(request, "bookstore/USERinfoPage.html", context)