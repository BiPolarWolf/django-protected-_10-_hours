from decimal import Decimal
from uuid import uuid4
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
import stripe
from yookassa import Configuration, Payment

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
Configuration.account_id = settings.YOOKASSA_SHOP_ID

from cart.cart import Cart
from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem


def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "payment/payment-success.html")


def payment_fail(request):
    return render(request, "payment/payment_fail.html")


def complete_order(request):
    if request.method == "POST":
        payment_type = request.POST.get("stripe-payment", "yookassa-payment")
        name = request.POST.get("name")
        email = request.POST.get("email")
        street_adress = request.POST.get("street_adress")
        apartment_adress = request.POST.get("apartment_adress")
        country = request.POST.get("country")
        city = request.POST.get("city")
        zip_code = request.POST.get("zipcode")
        cart = Cart(request)
        total_price = cart.get_total_price()

        match payment_type:
            case "stripe-payment":
                shipping_adress, _ = ShippingAdress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        "full_name": name,
                        "email": email,
                        "street_adress": street_adress,
                        "apartment_adress": apartment_adress,
                        "country": country,
                        "city": city,
                        "zip_code": zip_code,
                    },
                )

                session_data = {
                    "mode": "payment",
                    "success_url": request.build_absolute_uri(
                        reverse("payment:payment-success")
                    ),
                    "cancel_url": request.build_absolute_uri(
                        reverse("payment:payment-failed")
                    ),
                    "line_items": [],
                }

                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user,
                        shipping_adress=shipping_adress,
                        amount=total_price,
                    )

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            price=item["price"],
                            quantity=item["qty"],
                            user=request.user,
                        )

                        session_data["line_items"].append(
                            {
                                "price_data": {
                                    "unit_amount": int(item["price"] * Decimal(100)),
                                    "currency": "usd",
                                    "product_data": {"name": item["product"].title},
                                },
                                "quantity": item["qty"],
                            }
                        )

                    session = stripe.checkout.Session.create(
                        **session_data,
                    )
                    return redirect(session.url,code=303)

                else:
                    order = Order.objects.create(
                        shipping_adress=shipping_adress, amount=total_price
                    )

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            price=item["price"],
                            quantity=item["qty"],
                        )
            # yookassa
            case "yookassa-payment":
                idempotence_key = uuid4()
                currency="RUB"
                description = 'Товары в корзине'
                payment = Payment.create({
                    "amount": {
                        "value": str(total_price * 93),
                        "currency": currency
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": request.build_absolute_uri(reverse('payment:payment-success')),
                    },
                    "capture": True,
                    "test": True,
                    "description": description,
                }, idempotence_key)

                #create or get shipping_adress 
                shipping_adress, _ = ShippingAdress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        "full_name": name,
                        "email": email,
                        "street_adress": street_adress,
                        "apartment_adress": apartment_adress,
                        "country": country,
                        "city": city,
                        "zip_code": zip_code,
                    },
                )

                confirmation_url = payment.confirmation.confirmation_url

                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user,
                        shipping_adress=shipping_adress,
                        amount=total_price,
                    )

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            price=item["price"],
                            quantity=item["qty"],
                            user=request.user,
                        )
                    return redirect(confirmation_url)
                else:
                    order = Order.objects.create(
                        shipping_adress=shipping_adress, amount=total_price
                    )
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            price=item["price"],
                            quantity=item["qty"]
                        )
                    return redirect(confirmation_url)


@login_required(login_url="account:login")
def shipping(request):
    try:
        shipping_adress = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_adress = None

    form = ShippingAdressForm(instance=shipping_adress)

    if request.method == "POST":
        form = ShippingAdressForm(request.POST, instance=shipping_adress)
        if form.is_valid():
            shipping_adress = form.save(commit=False)
            shipping_adress.user = request.user
            shipping_adress.save()
            return redirect("account:dashboard")
    return render(request, "payment/shipping.html", {"form": form})


def checkout(request):
    if request.user.is_authenticated:
        shipping_adress = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_adress:
            return render(
                request, "payment/checkout.html", {"shipping_adress": shipping_adress}
            )

    return render(request, "payment/checkout.html")
