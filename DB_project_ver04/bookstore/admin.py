from django.contrib import admin
from .models import Card
from .models import User
from .models import Order
from .models import Book
from .models import ShoppingBasket
from .models import ShippingDestination
from .models import BookSB
from .models import BookOrder
from .models import Coupon

# Register your models here.
admin.site.register(User)
admin.site.register(ShippingDestination)
admin.site.register(Card)
admin.site.register(Order)
admin.site.register(ShoppingBasket)
admin.site.register(Book)
admin.site.register(BookSB)
admin.site.register(BookOrder)
admin.site.register(Coupon)