from user.apps import UserConfig
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet, PaymentViewSet

app_name = UserConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [] + router.urls
