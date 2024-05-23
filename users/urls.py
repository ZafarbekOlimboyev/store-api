from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserViewSet, ChangePasswordView, reset_password, update_user


router = DefaultRouter()

router.register('register', RegisterView)
router.register(prefix=r'user', viewset=UserViewSet, basename='user')

urlpatterns = router.urls
urlpatterns += [
    path('change-password/', ChangePasswordView.as_view()),
    path('reset-password/', reset_password),
    path('sign-up/<int:pk>', update_user)
]
