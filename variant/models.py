from django.db import models

from catalog_product.models import *
from pages.models import *


class ProductVariant(TimeStamp):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE)
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    variant_image = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        super(ProductVariant, self).save()

    class Meta:
        db_table = 'product_variant'


class ProductVariantCombination(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE)
    attribute = models.ForeignKey(
        Attributes, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(
        AttributeValues, on_delete=models.CASCADE)

    def save(self, **kwargs):
        super(ProductVariantCombination, self).save()

    class Meta:
        db_table = 'product_variants_combination'


class ProductVariantPrice(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE)
    express_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    value_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    standard_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=255, blank=True, null=True)

    def save(self, **kwargs):
        super(ProductVariantPrice, self).save()

    class Meta:
        db_table = 'product_variants_price'


class VariantAssociatedAttributes(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    attribute = models.ForeignKey(
        Attributes, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(
        AttributeValues, on_delete=models.CASCADE)

    def save(self, **kwargs):
        super(VariantAssociatedAttributes, self).save()

    class Meta:
        db_table = 'variant_associated_attributes'
