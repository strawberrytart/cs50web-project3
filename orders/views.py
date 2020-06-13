from django.http import HttpResponse, HttpResponseRedirect
from orders.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json

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
    if request.method == "POST":
        username = request.POST["username"] 
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) # will return None if failed
        if user is not None:#if authentication is successful
            login(request, user)#request object contains cookies, current login user...
            print(request.session.session_key)
            try:
                order=Order.objects.get(user=request.user, status="Initiated")
            except:
                order=Order(user=request.user)
                order.save()
                print("Initiated a new order for", request.user)
            else:
                print("An order currently exists.")
            if 'next' in request.POST:
                print(request.POST.get('next'))
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse("index"))#takes in name and redirects the urls
        else:# if not successful
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else: #GET request
        return render(request, "orders/login.html")

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def cart_view(request):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.get(user=user, status="Initiated")
        print(order.id)
        try:
            cart_items=Cart.objects.all().filter(order_id=order)
        except:
            cart_items=[]
            grand_total=0
        else:
            print("Success!")
            grand_total=0
            for item in cart_items:
                grand_total+=item.item_price
                print(grand_total)
            print(grand_total)
    else:
        grand_total=0.00
        try:
            request.session['cart_items']
            print("cart aint empty")
        except KeyError as error:
            print(error)
            cart_items=[]
        else:
            cart_items=request.session['cart_items']
            for item in cart_items:
                grand_total+=float(item["price"])
    return render(request, "orders/cart.html", {"cart_items": cart_items, "grandtotal":grand_total})

@login_required(login_url="login") #only logged in users can access this orders url. If not, must go through login page first.
def order_view(request):
    if request.method == 'POST':
        total=0
        user=request.user
        print(user)
        order=Order.objects.get(user=user, status="Initiated")
        try:
            cart=Cart.objects.all().filter(order_id=order.id)
            print(cart)
        except:
            print("Failed")
        else:
            for i in cart:
                total+=i.item_price
                print(total)
        print(total)
        order.status="Submitted" #change status to Submitted
        order.order_total=total # total sum of order
        order.time=datetime.now()
        order.save()
        message=Order.objects.filter(user=user).exclude(status="Initiated")#query for all user's orders except for the "Initiated" one
        order=Order(user=request.user)#create a new order for the user
        order.save()
        return render(request, "orders/order.html", {'message': message})
    else:
        # if it is a GET request
        error=""
        user=request.user
        message=[]
        try:
            #get user's orders that are already submitted
            order=Order.objects.filter(user=user).exclude(status="Initiated")
            print(order)
        except error:
            # else ,display error message
            print(error)
            error="No orders submitted for now."
        else:
            message=order
            # if successful, get the cart items through the related name "order_id"
            #message=order.order_id.all()
        return render(request, "orders/order.html", {'message': message})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            if 'next' in request.POST:
                print(request.POST.get('next'))
                return HttpResponseRedirect(request.POST.get('next'))
            else:
               return HttpResponseRedirect(reverse("login"))
    else:
        form = SignUpForm()
    return render(request, "orders/signup.html", {"form":form})

def manage_order(request):
    if request.method == 'POST':
        if 'mark' in request.POST:
            id=request.POST.get('mark')
            order=Order.objects.get(pk=id)
            order.status="Completed"
            order.save()
            orders=Order.objects.all()
    else:
        if request.user.is_superuser:
            orders=Order.objects.all()
            print(orders)
    return render(request, "orders/manage_order.html", {"orders":orders})


@login_required(login_url="login") #only logged in users can access this orders url. 
def order_summary(request):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.get(user=user, status="Initiated")
        order_id=order.id
        #here we will add in any items placed in the request session when the user was anon to the cart. 
        if request.session.get('cart_items', 0) != 0:
            guest_cart=request.session['cart_items']
            for item in guest_cart:
                dish=item['dish']
                price=item['price']
                toppings=item['toppings']
                print(dish, price, toppings)
                cart=Cart(order_id=order, user=user, cart_item=dish, item_price=price)
                cart.save()
                if len(toppings)>0:
                    toppings= toppings.split(", ")
                    for topping in toppings:
                        try:
                            t=Toppings.objects.get(name=topping)
                        except:
                            t=Extra.objects.get(name=topping)
                            cart.extras.add(t)
                        else:
                            cart.toppings.add(t)
            request.session['cart_items']=[]#clear the request session
        try:
            cart_items=Cart.objects.all().filter(order_id=order)
        except:
            cart_items=[]
            grand_total=0
        else:
            print("Success!")
            grand_total=0
            for item in cart_items:
                grand_total+=item.item_price
                print(grand_total)
            print(grand_total)
    else:
        grand_total=0.00
        try:
            request.session['cart_items']
            print("cart aint empty")
        except KeyError as error:
            print(error)
            cart_items=[]
        else:
            cart_items=request.session['cart_items']
            for item in cart_items:
                grand_total+=float(item["price"])
    return render(request, "orders/order_summary.html", {"cart_items": cart_items, "grandtotal":grand_total})



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
        message= request.POST['message']
        print(message)
        dish=request.POST['dish']
        price=request.POST['price']
        is_pizza=request.POST['flag']
        print(is_pizza)
        print(message)
        if request.is_ajax():
            if request.user.is_authenticated:
                user=request.user
                order=Order.objects.get(user=user, status="Initiated")
                order_id=order.id
                print("User:", user, "ID:", id)
                cart=Cart(order_id=order, user=user, cart_item=dish, item_price=price)
                cart.save()
                if len(message)>0:
                    if is_pizza == 'true':
                        toppings= message.split(", ")
                        print(toppings)
                        for topping in toppings:
                            t=Toppings.objects.get(name=topping)
                            cart.toppings.add(t)
                    else:
                        extras=message.split(", ")
                        print(extras)
                        for extra in extras:
                            e=Extra.objects.get(name=extra)
                            cart.extras.add(e)
            else:
                print("Anonymous User")
                if request.session.get('cart_items', 0) == 0:
                    print('session did not exists before')
                    request.session['cart_items']=[]
                a_list=request.session['cart_items']
                a_list.append({'dish':dish, 'price': price, 'toppings': message})
                request.session['cart_items']=a_list
                print(request.session['cart_items'])
            #add the user and order to Cart 
            return JsonResponse({'obj':'Successfully added item to cart!', 'dish':dish}, status=200)
        return HttpResponseRedirect(reverse("index"))

class DeleteCart(View):
    def post(self, request):
        id=request.POST['id']
        message="Error" #default message is Error
        if request.is_ajax():
            if request.user.is_authenticated:
                user=request.user
                try:
                    cart=Cart.objects.get(user=user, id=id) #get the cart based on user and the id of the item in the cart
                    cart.delete()
                except:
                    print("Failed to delete cart item.")
                else:
                    message='Sucessfully removed item from cart'
                return JsonResponse({'message':message}, status=200)
            else: # Guest trying to delete item from cart that is stored in the session. 
                try:
                    a_list=request.session['cart_items']
                except:
                    print('Error')
                else:
                    #remove item from session based on index clicked by the user    
                    a_list.pop(int(id)-1) #forloop counter indexed 1, so need to minus 1
                    request.session['cart_items']=a_list #update the 'cart_items' key in session
                    message='Sucessfully removed item from cart'
                return JsonResponse({'message':message}, status=200)
        return HttpResponseRedirect(reverse("cart_view"))