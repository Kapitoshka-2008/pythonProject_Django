from __future__ import annotations

from typing import Union

from django.db.models import QuerySet

from .models import Category, Product


def get_products_by_category(category: Union[Category, int]) -> QuerySet[Product]:
    """
    Return published products that belong to the given category.

    Args:
        category: Category instance or primary key.

    Returns:
        QuerySet with related category prefetched.
    """
    category_id = category if isinstance(category, int) else category.pk
    return Product.objects.select_related('category').filter(
        category_id=category_id,
        status=Product.PublicationStatus.PUBLISHED,
    )

