from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .models import *

router = DefaultRouter()
router.register('list', UserViewSet)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]