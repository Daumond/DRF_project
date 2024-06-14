from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from user.models import User, Payment
from user.serializers import UserSerializer, PaymentSerializer
from course.services import get_stripe, retrieve_stripe

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('pay_course', 'pay_lesson', 'pay_method', )

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Payment.objects.filter(user=self.request.user)
        elif self.request.user.is_staff:
            return Payment.objects.all()
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        if payment.pay_method == 'transfer':
            session = get_stripe(payment)
            payment.pay_url = session.url
            payment.session = session.id
        payment.save()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj.session:
            session = retrieve_stripe(obj.session)
            if session.payment_status == 'paid' and session.status == 'complete':
                obj.is_success = True
                obj.save()

        return obj
