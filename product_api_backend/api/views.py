from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_id='health',
    operation_summary='Health Check',
    operation_description='Returns a 200 with a simple message to indicate the server is running.',
    responses={200: openapi.Response(description="Health OK", schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
    ))},
    tags=['health']
)
@api_view(['GET'])
def health(request):
    """
    Health endpoint.
    Returns HTTP 200 and a JSON message indicating the server is up.
    """
    return Response({"message": "Server is up!"}, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet providing CRUD operations for Product.

    Endpoints:
    - GET /api/products/            -> list
    - POST /api/products/           -> create
    - GET /api/products/{id}/       -> retrieve
    - PUT /api/products/{id}/       -> update
    - PATCH /api/products/{id}/     -> partial_update
    - DELETE /api/products/{id}/    -> destroy
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
