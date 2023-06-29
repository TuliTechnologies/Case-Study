from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # newly added 
# from digital_press import settings
# from django.conf import Setting 

class TimeStamp(models.Model):
    """Base class containing all models common information."""
    is_active = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True,default=True) # newly added 
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    

    class Meta:
        """Define Model as abstract."""
        abstract = True


class Brands(TimeStamp):
    logo = models.TextField()
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()

    def save(self, **kwargs):
        super(Brands, self).save()

    class Meta:
        db_table = 'brands'


class Categories(TimeStamp):
    name = models.CharField(max_length=255)
    parent = models.PositiveIntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True)
    header_image = models.FileField(upload_to='category_images/',
                             null=True, verbose_name="")
    category_image = models.FileField(upload_to='category_images/single',
                             null=True, verbose_name="")
    header_text = models.TextField(null=True, blank=True)
    header_description = models.TextField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    show_on_home_page = models.BooleanField(default=False)
    # show_a_to_z_category = models.BooleanField(default=False, null=True)

    def save(self, **kwargs):
        super(Categories, self).save()

    class Meta:
        db_table = 'categories'


class Attributes(TimeStamp):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)

    def save(self, **kwargs):
        super(Attributes, self).save()

    class Meta:
        db_table = 'attributes'


class AttributeValues(TimeStamp):
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, related_name='attribute_values')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def save(self, **kwargs):
        super(AttributeValues, self).save()

    class Meta:
        db_table = 'attribute_values'


class ProductTypes(TimeStamp):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def save(self, **kwargs):
        super(ProductTypes, self).save()

    class Meta:
        db_table = 'product_types'

class ProductTypeAttributeValue(TimeStamp):
    product_type = models.ForeignKey(ProductTypes, on_delete=models.CASCADE, related_name='product_type')
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, related_name='attributes')
    attribute_value = models.ForeignKey(AttributeValues, on_delete=models.CASCADE, related_name='attribute_values')

    def save(self, **kwargs):
        super(ProductTypeAttributeValue, self).save()

    class Meta:
        db_table = 'product_type_attribute_values'

class ShippingType(TimeStamp):
    type = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    days = models.PositiveIntegerField(blank=True, null=True)

    def save(self, **kwargs):
        super(ShippingType, self).save()

    class Meta:
        db_table = 'shipping_type'

class CategoryFAQ(TimeStamp):
    category_id = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='faq')
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    
    def save(self, **kwargs):
        super(CategoryFAQ, self).save()

    class Meta:
        db_table = 'category_faq'
