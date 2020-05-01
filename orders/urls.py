from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_page, name="login"),
    path("login_verify", views.login_verify, name="login-verify"),
    path("logout", views.logout_view, name="logout"),
    path("cart", views.cart_view, name="cart_view"),
    path("orders", views.order_view, name="order_view"),
    path("signup", views.sign_up, name="sign_up"),
    path("modal", views.Modal.as_view()),
    path("modal_other", views.ModalOther.as_view()),
    path("add_to_cart", views.AddToCart.as_view())
]
