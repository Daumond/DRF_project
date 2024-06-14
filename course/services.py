import stripe

from DRF_project import settings
from course.models import Lesson
from user.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def get_stripe(serializer: Payment):
    """ Внешнее API Stripe оплата курса или урока"""
    product_name = serializer.course.name if serializer.course else serializer.lesson.name
    product_price = serializer.course.price_course if serializer.course else serializer.lesson.price_lesson
    product = stripe.Product.create(name=product_name)
    price = stripe.Price.create(
        unit_amount=product_price * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[{'price': price.id, 'quantity': 1, }],
        mode='payment',

    )

    return session


def retrieve_stripe(session_id):
    """ Получаем ответ Stripe"""
    return stripe.checkout.Session.retrieve(session_id)
