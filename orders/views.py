from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View
from .forms import OrderForm
from .models import Order, OrderItem
from cart.views import CartMixin
from cart.models import Cart
from main.models import ProductSize
from decimal import Decimal
from payment.views import create_stripe_checkout_session


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class CheckoutView(CartMixin, View):

    def get_context(self, request, cart, form, **extra):
        context = {
            'form': form,
            'cart': cart,
            'cart_items': cart.items.select_related(
                'product', 'product_size__size'
            ).order_by('-added_at'),
            'total_price': cart.subtotal,
        }
        context.update(extra)
        return context

    def render_response(self, request, context):
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'orders/checkout_content.html', context)
        return render(request, 'orders/checkout.html', context)

    def get(self, request):
        cart = self.get_cart(request)

        if cart.total_items == 0:
            if request.headers.get('HX-Request'):
                return TemplateResponse(request, 'orders/empty_cart.html', {'message': 'Your cart is empty.'})
            return redirect('cart:cart_modal')

        form = OrderForm(user=request.user)
        context = self.get_context(request, cart, form)
        return self.render_response(request, context)

    def post(self, request):
        cart = self.get_cart(request)
        payment_provider = request.POST.get('payment_provider')

        if cart.total_items == 0:
            if request.headers.get('HX-Request'):
                return TemplateResponse(request, 'orders/empty_cart.html', {'message': 'Your cart is empty.'})
            return redirect('cart:cart_modal')

        if not payment_provider or payment_provider not in ['stripe']:
            form = OrderForm(user=request.user)
            context = self.get_context(request, cart, form,
                error_message='Please select a valid payment provider.')
            return self.render_response(request, context)

        form_data = request.POST.copy()
        if not form_data.get('email'):
            form_data['email'] = request.user.email
        form = OrderForm(form_data, user=request.user)

        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                company=form.cleaned_data.get('company', ''),
                address1=form.cleaned_data.get('address1', ''),
                address2=form.cleaned_data.get('address2', ''),
                city=form.cleaned_data.get('city', ''),
                country=form.cleaned_data.get('country', ''),
                province=form.cleaned_data.get('province', ''),
                postal_code=form.cleaned_data.get('postal_code', ''),
                phone=form.cleaned_data.get('phone', ''),
                special_instructions='',
                total_price=cart.subtotal,
                payment_provider=payment_provider,
            )

            for item in cart.items.select_related('product', 'product_size__size'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.product_size,
                    quantity=item.quantity,
                    price=item.product.price or Decimal('0.00')
                )

            try:
                if payment_provider == 'stripe':
                    checkout_session = create_stripe_checkout_session(order, request)
                    if request.headers.get('HX-Request'):
                        response = HttpResponse(status=200)
                        response['HX-Redirect'] = checkout_session.url
                        return response
                    return redirect(checkout_session.url)

            except Exception as e:
                order.delete()
                context = self.get_context(request, cart, form,
                    error_message=f'Payment processing error: {str(e)}')
                return self.render_response(request, context)

        else:
            context = self.get_context(request, cart, form,
                error_message='Please correct the errors on the form.')
            return self.render_response(request, context)