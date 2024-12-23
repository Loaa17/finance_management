from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BonusRequestViewSet
from .auth import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bonus-requests', BonusRequestViewSet, basename='bonus-requests')

app_name = 'finance'

urlpatterns = [
    path('', include(router.urls)),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]