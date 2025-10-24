from django.db import models


class Product(models.Model):
    """
    Product model representing a sellable item.

    Fields:
    - id: Auto-generated primary key (BigAutoField from project default)
    - name: Name of the product
    - price: Decimal price with 10 total digits and 2 decimal places
    - quantity: Available stock quantity
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 99999999.99 max
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} (${self.price}) x{self.quantity}"
