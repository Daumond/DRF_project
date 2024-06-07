from django.urls import path
from user.apps import UserConfig
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import UserViewSet, PaymentViewSet

app_name = UserConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
