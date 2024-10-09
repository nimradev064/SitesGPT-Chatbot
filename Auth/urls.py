from rest_framework import routers
from .views import RegisterView , Login , ActivationCodeView

router = routers.DefaultRouter()

router.register('SignUp', RegisterView, basename='signup')
router.register('Login', Login, basename='Login')
router.register('ActivationCode', ActivationCodeView, basename='ActivationCode')




urlpatterns = router.urls