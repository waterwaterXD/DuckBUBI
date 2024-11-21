from .APIset import TrainingResultViewSet,EventResultViewSet,LoginAPIView
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'TrainingResult', TrainingResultViewSet, basename='TrainingResult')
router.register(r'EventResult', EventResultViewSet, basename='EventResult')
urlpatterns = router.urls

urlpatterns += [path('login/', LoginAPIView.as_view(), name='login_api'),]