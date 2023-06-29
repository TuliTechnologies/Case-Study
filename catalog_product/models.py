from django.db import models
from pages.models import TimeStamp, Brands, Categories, ProductTypes, Attributes, AttributeValues, ProductTypeAttributeValue
from supplier.models import Supplier
from django_mysql.models import ListCharField
from django.db.models import CharField, Model


class Products(TimeStamp):
    
    PRODUCT_STATUS = (
        ('draft', 'draft'),
        ('archive', 'archive'),
        ('active', 'active')
    )

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        ProductTypes, on_delete=models.CASCADE,  related_name='attributes_variants', null=True, blank=True)
    name = models.CharField('Name', max_length=255)
    short_name = models.CharField(max_length=255, null=True)
    sku = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    short_description = models.TextField(null=True)
    feature_image = models.TextField(null=True, blank=True)
    feature_img_thumb = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    key_features = models.TextField(null=True, blank=True)
    product_specs = models.TextField(null=True, blank=True)
    submission_specs = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    print_area = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    lead_time = models.CharField(max_length=255, blank=True, null=True)
    carriage = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(null=False, default=1)
    is_active = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_vat_applicable = models.BooleanField(default=False)
    status = models.CharField(max_length=23, choices=PRODUCT_STATUS, default=PRODUCT_STATUS[0][0])
    weight = models.CharField(max_length=255, blank=True, null=True)
    prod_weight = models.IntegerField(null=True, blank=True)
    show_a_to_z_category = models.BooleanField(default=False, null=True)
    url_3d = models.TextField(null=True, blank=True)
    is_delivery_applicable = models.BooleanField(default=False, null=True)
    video_url = models.TextField(null=True, blank=True)
    video_description = models.TextField(null=True, blank=True)
    video_title = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        super(Products, self).save()

    class Meta:
        db_table = 'products'

class DeliveryMethods(TimeStamp):
    
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_delivery_methods', null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    days = models.CharField(max_length=255, blank=True, null=True)

    def save(self, **kwargs):
        super(DeliveryMethods, self).save()

    class Meta:
        db_table = 'delivery_methods'
    
class DeliverySettings(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_delivery_settings', null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    days = models.CharField(max_length=255, blank=True, null=True)

    def save(self, **kwargs):
        super(DeliverySettings, self).save()

    class Meta:
        db_table = 'delivery_settings'

class DesignService(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_design_service', null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)

    def save(self, **kwargs):
        super(DesignService, self).save()

    class Meta:
        db_table = 'design_service'

class ProductImages(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_images', null=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='product_images/',
                             null=True, verbose_name="")

    def save(self, **kwargs):
        super(ProductImages, self).save()

    class Meta:
        db_table = 'product_images'


class Artworks(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='artworks')
    type = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='artworks/', null=True, verbose_name="")
    # old one ------
    ai = models.FileField(upload_to='artworks/ai/', null=True, verbose_name="")
    indd = models.FileField(upload_to='artworks/indd/',
                            null=True, verbose_name="")
    pdf = models.FileField(upload_to='artworks/pdf/',
                           null=True, verbose_name="")
    psd = models.FileField(upload_to='artworks/psd/',
                           null=True, verbose_name="")

    def save(self, **kwargs):
        super(Artworks, self).save()

    class Meta:
        db_table = 'artworks'

class FAQ(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='faq')
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    
    def save(self, **kwargs):
        super(FAQ, self).save()

    class Meta:
        db_table = 'faq'


class ProductDesign(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_design')
    image_url = models.FileField(upload_to='product_designs/', null=True, verbose_name="")
    name = models.TextField(null=True)
    design_position = models.CharField('Name', max_length=255)
    left_px = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    top_px = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    width_px = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    height_px = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    width_in = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    height_in = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    top_in = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    left_in = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    image_height = models.DecimalField(
        max_digits=12, decimal_places=5, null=True)
    image_width = models.DecimalField(
        max_digits=12, decimal_places=5, null=True)

    def save(self, **kwargs):
        super(ProductDesign, self).save()

    class Meta:
        db_table = 'product_design'


class ProductAttribute(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(
        Attributes, on_delete=models.CASCADE, related_name='product_attribute_id')

    def save(self, **kwargs):
        super(ProductAttribute, self).save()

    class Meta:
        db_table = 'product_attribute'


class ProductAttributeValue(TimeStamp):
    product_attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE)
    attribute_value_id = models.IntegerField(null=True, blank=True)

    def save(self, **kwargs):
        super(ProductAttributeValue, self).save()

    class Meta:
        db_table = 'product_attribute_value'


class ProductVariants(TimeStamp):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_variant')
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    def save(self, **kwargs):
        super(ProductVariants, self).save()

    class Meta:
        db_table = 'product_variants'


class ProductVariantBase(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariants, on_delete=models.CASCADE, related_name='product_variant_base')
    base_attribute_id = models.PositiveIntegerField(null=True, blank=True)
    base_attribute_value_id = models.PositiveIntegerField(
        null=True, blank=True)
    attribute = models.ForeignKey(
        Attributes, on_delete=models.CASCADE, related_name='product_attribute')
    attribute_value = models.ForeignKey(
        AttributeValues, on_delete=models.CASCADE, related_name='product_attribute_value')

    def save(self, **kwargs):
        super(ProductVariantBase, self).save()

    class Meta:
        db_table = 'product_variants_base'


class ProductVariantSKU(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariants, on_delete=models.CASCADE, related_name='product_variant_sku')
    price = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    express_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    value_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    standard_price = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        super(ProductVariantSKU, self).save()

    class Meta:
        db_table = 'product_variants_sku'


class ShippingDetails(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='shipping_details')
    product_variants = models.ForeignKey(
        ProductVariants, on_delete=models.CASCADE)
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    def save(self, **kwargs):
        super(ShippingDetails, self).save()

    class Meta:
        db_table = 'shipping_details'


class VariantsImages(TimeStamp):
    product_design_id = models.ForeignKey(
        ProductDesign, on_delete=models.CASCADE, related_name='variant_images')
    attribute_id = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    attribute_value_id = models.ForeignKey(
        AttributeValues, on_delete=models.CASCADE)
    image_file = models.TextField()

    def save(self, **kwargs):
        super(VariantsImages, self).save()

    class Meta:
        db_table = 'variants_images'


class ProductPriceConfigrations(TimeStamp):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price_uom = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    min_qty = models.IntegerField(null=True)
    max_qty = models.IntegerField(null=True)
    expiry_date = models.DateTimeField('DT Expiry', blank=True, null=True)

    def save(self, **kwargs):
        super(ProductPriceConfigrations, self).save()

    class Meta:
        db_table = 'product_price_configrations'


class SupplierProducts(TimeStamp):
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='product_supplier', null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    base_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    lead_time = models.CharField(max_length=255, null=True, blank=True)

    def save(self, **kwargs):
        super(SupplierProducts, self).save()

    class Meta:
        db_table = 'supplier_product'
