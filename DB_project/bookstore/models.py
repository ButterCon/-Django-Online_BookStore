from django.db import models
from django.utils.timezone import now

class User(models.Model):
    User_id = models.CharField(default='', max_length=50)
    User_pw = models.CharField(max_length=100)
    User_name = models.CharField(max_length=100)
    Select_SD_id = models.IntegerField(default=0)
    Select_Card_id = models.IntegerField(default=0)

    def __str__(self):
        return self.User_id


class ShippingDestination(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SD_num = models.IntegerField(default=0)
    SD_ba = models.CharField(max_length=100)
    SD_da = models.CharField(max_length=100)

    def __id__(self):
        return self.SD_id


class Card(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Card_name = models.CharField(max_length=100)
    Card_num = models.IntegerField(default=0)
    Card_date = models.CharField(max_length=100)

    def __id__(self):
        return self.id


class Order(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Order_date = models.DateTimeField(default=now, blank=True)
    Order_totalprice = models.IntegerField(default=0)
    Order_DC_totalprice = models.IntegerField(default=0)
    Order_DP = models.IntegerField(default=0)
    Order_con = models.BooleanField(default=0)

    def __id__(self):
        return self.id


class ShoppingBasket(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __id__(self):
        return self.id


class Book(models.Model):
    Book_name = models.CharField(max_length=100)
    Book_price = models.IntegerField(default=0)
    Book_stock = models.IntegerField(default=5)

    def __id__(self):
        return self.id


class BookSB(models.Model):         #책 장바구니 리스트
    Book = models.ForeignKey(Book, on_delete=models.PROTECT)
    ShoppingBasket = models.ForeignKey(ShoppingBasket, on_delete=models.PROTECT)
    BookSB_type = models.BooleanField(default=1)#0은 즉시구매, 1은 장바구니 구매

    def __id__(self):
        return self.id


class BookOrder(models.Model):      #책 주문내역리스트
    Book = models.ForeignKey(Book, on_delete=models.PROTECT)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    BO_count = models.IntegerField(default=0)   #책 수량
    BO_price = models.IntegerField(default=0)   #책 더한 가격
    CP_kind = models.CharField(default='', max_length=100)
    BO_DC_price = models.IntegerField(default=0)

    def __id__(self):
        return self.id


class Coupon(models.Model): #쿠폰
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    CP_kind = models.CharField(max_length=100)
    # 0)미사용, 1)사용대기, 2)사용완료
    CP_state = models.IntegerField(default=0)
    CP_date = models.DateTimeField()    #사용 날짜
    CP_validity = models.CharField(max_length=100)  #유효기간

    def __id__(self):
        return self.id


class DongseoPay(models.Model): #동서페이
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    DP_TradingDate = models.DateTimeField(default=now, blank=True)
    DP_ChargePrice = models.IntegerField(default=0) #마지막 충전액
    DP_UsedPrice = models.IntegerField(default=0)   #사용액
    DP_price = models.IntegerField(default=0)   #잔액
    DP_history = models.IntegerField(default=0) #주문목록id넣기

    def __id__(self):
        return self.id