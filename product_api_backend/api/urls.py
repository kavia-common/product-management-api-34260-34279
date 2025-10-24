from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, ProductViewSet

router = DefaultRouter()
# This will create routes:
# /api/products/ [GET, POST]
# /api/products/{id}/ [GET, PUT, PATCH, DELETE]
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('health/', health, name='Health'),
    path('', include(router.urls)),
]
