from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.decorators import login_required #для того чтоб токо зарег юзеры могли оформ заказ
from main.models import Size
from django.conf import settings 
import stripe


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY #это чтоб подкл к апи страйп и юзать его в проекте


@login_required(login_url='/users/login')#l_req чтобы ток авториз пользователи могли получить к ним доступа если они не авториз то l_url перенапрл в (кудато(на авториз))
def order_create(request):
    cart = Cart(request)
    total_price = sum(item['total_price'] for item in cart) #проход по всей корзине

    if request.method == 'POST':  #если чел нажмёт оформ заказ то будет ниже
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                first_name = form.cleaned_data.get('first_name'), #cl_data использ в формах для доступа к данным, которые были валидированы
                last_name = form.cleaned_data.get('last_name'),
                middle_name = form.cleaned_data.get('middle_name'),
                city = form.cleaned_data.get('city'),
                street = form.cleaned_data.get('street'),
                house_number = form.cleaned_data.get('house_number'),
                postal_code = form.cleaned_data.get('postal_code'),
            )
            order.save()

            for item in cart:  #берём объекты из корзины
                size_instance = Size.objects.get(name=item['size'])
                OrderItem.objects.create(  #ниже заполн параметры OrItem
                    order=order,
                    clothing_item=item['item'], #по ключу получ
                    size=size_instance,
                    quantity=item['quantity'],
                    total_price=item['total_price'],
                )

            try: #созд сессию в страйпе 
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data':{ 
                                'currency': 'usd',
                                'product_data': {
                                    'name':item['item'].name,
                                },
                                'unit_amount': int(item['total_price'] * 100),
                            },
                            'quantity': item['quantity'],
                        } for item in cart
                    ],
                    mode='payment',
                    success_url='http://localhost:8000/orders/completed',
                    cancel_url='http://localhost:8000/orders/create',
                )  

                return redirect(session.url, code=303)
            except Exception as e:#тут сокр ошибка
                return render(request, 'orders/order_form.html', {
                    'form': form,
                    'cart': cart,
                    'error': str(e),
                })
            
    form = OrderForm(initial={  #форма для иниц даннных профиля если чел зарег и снова заход
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'middle_name': request.user.middle_name,
        'city': request.user.city,
        'street': request.user.street,
        'house_number': request.user.house_number,
        'apartment_number': request.user.apartment_number,
        'postal_code': request.user.postal_code,
    })            
    
    return render(request, 'orders/order_form.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })


@login_required(login_url='/users/login')
def order_success(request): 
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order_success.html')