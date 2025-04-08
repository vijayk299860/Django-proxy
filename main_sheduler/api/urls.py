from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main_sheduler.api import views
from rest_framework.viewsets import ModelViewSet

router = DefaultRouter()

# urls.py

router = DefaultRouter()
router.register(r'credentials', views.EmailCredentialViewSet)
router.register(r'scheduled-emails', views.ScheduledEmailViewSet)

urlpatterns = [
    path('mail/', include(router.urls)),
]
