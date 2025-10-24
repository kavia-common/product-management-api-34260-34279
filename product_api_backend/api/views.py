from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum, F
from django.db.models.functions import Coalesce

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
    - GET /api/products/total-balance/ -> total balance across all products (price * quantity)
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    # PUBLIC_INTERFACE
    @action(detail=False, methods=['get'], url_path='total-balance', permission_classes=[AllowAny])
    @swagger_auto_schema(
        method='get',
        operation_id='products_total_balance',
        operation_summary='Get total balance of inventory',
        operation_description='Returns the total monetary value across all products as SUM(price * quantity). Result is a decimal string.',
        responses={
            200: openapi.Response(
                description="Total balance computed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_balance': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format='decimal',
                            description='Total balance as decimal string'
                        )
                    }
                )
            )
        },
        tags=['products']
    )
    def total_balance(self, request):
        """
        Compute and return the total balance across all products.
        The total is computed using SUM(price * quantity). If there are no products, returns 0.
        Returns:
            { "total_balance": "<decimal string>" }
        """
        # Use ORM aggregation to compute SUM(price * quantity), coalesce to 0 if None.
        total = Product.objects.aggregate(
            total=Coalesce(Sum(F('price') * F('quantity')), 0)
        )['total']

        # Ensure Decimal-safe serialization by converting to string
        return Response({'total_balance': str(total)}, status=status.HTTP_200_OK)
