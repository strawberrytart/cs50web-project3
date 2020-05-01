from django.contrib import admin

# Register your models here.
from .models import Salads, Pasta, Toppings, DinnerPlatters, RegularPizza, SicilianPizza, Subs, Extra, Order, Cart, OrderAdmin

admin.site.register(Salads)
admin.site.register(Pasta)
admin.site.register(Toppings)
admin.site.register(DinnerPlatters)
admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(Subs)
admin.site.register(Order, OrderAdmin)
admin.site.register(Extra)
admin.site.register(Cart)