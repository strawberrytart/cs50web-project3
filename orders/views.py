from django.http import HttpResponse, HttpResponseRedirect
from orders.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View

from .models import Salads, Pasta, Toppings, DinnerPlatters, RegularPizza, SicilianPizza, Subs, Extra, Order, Cart

# Create your views here.
def index(request):
    if not request.user.is_authenticated:# if user has not logged in 
        context={
            "user":None,
            "regularpizzas": RegularPizza.objects.all(),
            "sicilianpizzas": SicilianPizza.objects.all(),
            "subs":Subs.objects.all(),
            "extras": Extra.objects.all(),
            "orders": Order.objects.all(),
            "carts": Cart.objects.all(),
            "dinner_platters": DinnerPlatters.objects.all(),
            "toppings": Toppings.objects.all(),
            "pastas": Pasta.objects.all(),
            "salads":Salads.objects.all()
        }
        return render(request, "orders/index.html", context)
    # else if user has logged in
    context ={ 
        "user": request.user,
        "regularpizzas": RegularPizza.objects.all(),
        "sicilianpizzas": SicilianPizza.objects.all(),
        "subs":Subs.objects.all(),
        "extras": Extra.objects.all(),
        "orders": Order.objects.all(),
        "carts": Cart.objects.all(),
        "dinner_platters": DinnerPlatters.objects.all(),
        "toppings": Toppings.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads":Salads.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_page(request):
    return render(request, "orders/login.html")

def login_verify(request):#request contains session cookies...
    username = request.POST["username"] 
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password) # will return None if failed
    if user is not None:#if authentication is successful
        login(request, user)#request object contains cookies, current login user...
        return HttpResponseRedirect(reverse("index"))#takes in name and redirects the urls
    else:# if not successful
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def cart_view(request):

  




    return render(request, "orders/cart.html")


def order_view(request):






    return render(request, "orders/cart.html")

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse("login"))
    else:
        form = SignUpForm()
    return render(request, "orders/signup.html", {"form":form})



class Modal(View):
    def get(self, request):
        name= request.GET.get('name')
        a=request.GET.get('button_class')
        print(a)
        n=0
        header=""
        if request.is_ajax():
            try:
                int(name[0])
            except ValueError:
                pass
            else:
                n=int(name[0])
            print(n)
            if "item" in name:
                header="item"
            elif "topping" in name:
                header="topping"
            toppings=Toppings.objects.values()
            return JsonResponse({'toppings': list(toppings), 'n':n}, status=200)
        return HttpResponseRedirect(reverse("index"))


class ModalOther(View):
    def get(self, request):
        buttonclass=request.GET.get('button_class')
        load=""
        if request.is_ajax():
            if buttonclass=="subs":
                load=list(Extra.objects.values())
            else:
                pass
            return JsonResponse({'obj':load}, status=200)
        return HttpResponseRedirect(reverse("index"))

class AddToCart(View):
    def post(self, request):
        toppings_0= request.POST['toppings_0']
        toppings_1= request.POST['toppings_1']
        toppings_2= request.POST['toppings_2']

        if request.is_ajax():
            print(toppings_0, toppings_1, toppings_2)
            #add the user and order to Cart 
            return JsonResponse({'obj':'Successfully added item to cart!'}, status=200)
        return HttpResponseRedirect(reverse("index"))

