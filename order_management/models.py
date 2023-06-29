from django.db import models
from pages.models import TimeStamp
from catalog_product.models import Products
from accounts.models import Users
from supplier.models import Supplier
# import uuid

class CustomerAddress(TimeStamp):
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    address1 = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    zip = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=255, null=True)
    province_code = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255, null=True)
    pobox = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    postal_code_type = models.CharField(max_length=255, null=True)
   
    def save(self, **kwargs):
        super(CustomerAddress, self).save()

    class Meta:
        db_table = 'customer_addresses'


class CreditCard(TimeStamp):

    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    cc_number = models.CharField(max_length=255, null=True)
    cc_type = models.CharField(max_length=255, null=True)
    cc_exp_date = models.DateField(null=False)
    cc_name = models.CharField(max_length=255, null=True)
    cc_display_number = models.CharField(max_length=255, null=True)
    cc_company = models.CharField(max_length=255, null=True)
    billing_geocode = models.CharField(max_length=255, null=True)
    billing_street1 = models.CharField(max_length=255, null=True)
    billing_street2 = models.CharField(max_length=255, null=True)
    billing_city = models.CharField(max_length=255, null=True)
    billing_state = models.CharField(max_length=255, null=True)
    billing_country = models.CharField(max_length=255, null=True)
    billing_pobox = models.CharField(max_length=255, null=True)
    billing_postal_code = models.CharField(max_length=255, null=True)
    billing_postal_code_type = models.CharField(max_length=255, null=True)
    map_key = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'credit_cards'


class ShippingMethod(TimeStamp):

    carrier = models.CharField(max_length=255, null=True)
    method = models.CharField(max_length=255, null=True)
    average_shipping_time = models.PositiveIntegerField(
        null=False, default=0)  # in seconds
    price_value = models.DecimalField(max_digits=6, decimal_places=2)
    price_currency = models.CharField(max_length=255, null=True)
    weight_limit = models.DecimalField(max_digits=6, decimal_places=2)
    restrictions = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    po_box_allowed = models.BooleanField(null=False, default=False)
    signature_required = models.BooleanField(null=False, default=False)
    saturday_delivery = models.BooleanField(null=False, default=False)
    international_delivery = models.BooleanField(null=False, default=False)
    size_limit = models.DecimalField(max_digits=6, decimal_places=2)
    packaging_type = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'shipping_methods'


class DiscountSet(TimeStamp):

    discount_set_name = models.CharField(max_length=255, null=True)
    xml_definition = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'discount_sets'


class Discount(TimeStamp):

    discount_set = models.ForeignKey(DiscountSet, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=255, null=True)
    discount_name = models.CharField(max_length=255, null=True)
    is_global = models.BooleanField(null=False, default=False)
    priority = models.BooleanField(null=False, default=False)
    allowed_uses = models.PositiveIntegerField(null=False, default=0)
    modifier = models.CharField(max_length=255, null=True)
    discount_rule = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(null=False, default=False)
    description = models.TextField(null=True)
    display_description = models.TextField(null=True)

    class Meta:
        db_table = 'discounts'


class DiscountAssociation(TimeStamp):

    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    use_count = models.PositiveIntegerField(null=False, default=0)
    display_description = models.TextField(null=True)

    class Meta:
        db_table = 'discount_associations'


class Transaction(TimeStamp):

    batch_id = models.CharField(max_length=255, null=True, blank=True)
    tran_date = models.DateField(null=True, blank=True)
    tran_status = models.CharField(max_length=255, null=True, blank=True)
    tran_amount = models.DecimalField(max_digits=6, decimal_places=2)
    tran_currency = models.CharField(max_length=255, null=True, blank=True)
    cc_number = models.CharField(max_length=255, null=True, blank=True)
    cc_type = models.CharField(max_length=255, null=True, blank=True)
    cc_exp_date = models.DateField(null=True, blank=True)
    cc_name = models.CharField(max_length=255, null=True, blank=True)
    cc_display_number = models.CharField(max_length=255, null=True, blank=True)
    cc_company = models.CharField(max_length=255, null=True, blank=True)
    geocode = models.CharField(max_length=255, null=True, blank=True)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pobox = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    postal_code_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'transactions'


class TransactionEntry(TimeStamp):

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    tran_entry_sequence = models.CharField(max_length=255, null=True)
    tran_entry_date = models.DateField(null=True, blank=True)
    tran_entry_status = models.CharField(max_length=255, null=True)
    tran_entry_amount = models.DecimalField(max_digits=6, decimal_places=2)
    tran_entry_currency = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'transaction_entries'


class Order(TimeStamp):

    ORDER_STATUS = (
        ('received', 'received'),
        ('in_review', 'in_review'),
        ('accepted', 'accepted'),
        ('cancelled', 'cancelled'),
        ('in_production', 'in_production'),
        ('shipped', 'shipped'),
        ('delayed', 'delayed'),
        ('delivered', 'delivered'),
        ('refund', 'refund')
    )
    customer = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="user")
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=23, choices=ORDER_STATUS, default=ORDER_STATUS[1][0])
    order_date = models.DateField(null=True, blank=True)
    shipping_method = models.CharField(max_length=255, null=True)
    shipping_amount = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_currency = models.CharField(max_length=255, null=True)
    price_amount = models.DecimalField(max_digits=6, decimal_places=2)
    price_currency = models.CharField(max_length=255, null=True)
    shipping_geocode = models.CharField(max_length=255, null=True)
    shipping_street1 = models.CharField(max_length=255, null=True)
    shipping_street2 = models.CharField(max_length=255, null=True)
    shipping_city = models.CharField(max_length=255, null=True)
    shipping_state = models.CharField(max_length=255, null=True)
    shipping_country = models.CharField(max_length=255, null=True)
    shipping_pobox = models.CharField(max_length=255, null=True)
    shipping_county = models.CharField(max_length=255, null=True)
    shipping_postal_code = models.CharField(max_length=255, null=True)
    shipping_postal_code_type = models.CharField(max_length=255, null=True)
    special_instructions = models.CharField(max_length=255, null=True)
    splitting_preference = models.CharField(max_length=255, null=True)
    order_subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    new_order = models.BooleanField(null=False, default=True)

    class Meta:
        db_table = 'orders'


class OrderItem(TimeStamp):

    ORDER_STATUS = (
        ('received', 'received'),
        ('in_review', 'in_review'),
        ('accepted', 'accepted'),
        ('cancelled', 'cancelled'),
        ('in_production', 'in_production'),
        ('shipped', 'shipped'),
        ('delayed', 'delayed'),
        ('delivered', 'delivered'),
        ('refund', 'refund')
    )

    SELLER_PAYMENT_STATUS = (
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('refunded', 'refunded'),
        ('authorized', 'authorized'),
        ('failed', 'failed'),
        ('cancelled', 'cancelled'),
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='supplier')
    external_order_id = models.CharField(max_length=255, null=True)
    order_quotation_id = models.CharField(max_length=255, null=True)
    catalog_product_id = models.CharField(max_length=255, null=True)
    catalog_product_variant_id = models.CharField(max_length=255, null=True)
    product_id = models.CharField(max_length=255, null=True)
    variant_id = models.CharField(max_length=255, null=True)
    external_product_id = models.CharField(max_length=255, null=True)
    external_variant_id = models.CharField(max_length=255, null=True)
    inventory_location_id = models.CharField(max_length=255, null=True)
    vendor_id = models.CharField(max_length=255, null=True)
    vendor_order_id = models.CharField(max_length=255, null=True)
    options = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    product_name = models.CharField(max_length=255, null=True)
    variant_name = models.CharField(max_length=255, null=True)
    sku = models.CharField(max_length=255, null=True)
    weight_unit = models.CharField(max_length=255, null=True)
    weight = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    total_weight = models.DecimalField(
        max_digits=16, decimal_places=2,  null=True, blank=True)
    weight_in_grams = models.DecimalField(
        max_digits=16, decimal_places=2,  null=True, blank=True)
    total_weight_in_grams = models.DecimalField(
        max_digits=16, decimal_places=2,  null=True, blank=True)
    item_price = models.DecimalField(
        max_digits=16, decimal_places=2,  null=True, blank=True)
    qty_ordered = models.PositiveIntegerField(null=False, default=0)
    item_total_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    discount_details = models.CharField(max_length=255, null=True, blank=True)
    subtotal_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    tax_details = models.CharField(max_length=255, null=True)
    buyer_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    can_refund = models.BooleanField(null=False, default=False)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancel_reason = models.TextField(blank=True, null=True)
    qty_refunded = models.PositiveIntegerField(null=False, default=0)
    refund_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    refund_details = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=23, choices=ORDER_STATUS, default=ORDER_STATUS[1][0])
    status_at = models.DateTimeField(blank=True, null=True)
    seller_name = models.CharField(max_length=255, null=True, blank=True)
    seller_email = models.CharField(max_length=255, null=True, blank=True)
    seller_item_price = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_item_total_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_discount_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_discount_details = models.TextField(blank=True, null=True)
    seller_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_amount_paid = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_refund_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True)
    seller_refund_details = models.TextField(blank=True, null=True)
    seller_payment_status = models.CharField(
        max_length=18, choices=SELLER_PAYMENT_STATUS, default=SELLER_PAYMENT_STATUS[1][0])
    notes = models.TextField(blank=True, null=True)
    vendor_name = models.CharField(max_length=255, null=True)
    vendor_email = models.CharField(max_length=255, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    close_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'order_items'


class OrderItemDesigns(TimeStamp):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    design_key = models.CharField(max_length=255, null=True)
    catalog_design_file_id = models.CharField(max_length=255, null=True)
    catalog_design_file_url = models.CharField(max_length=255, null=True)
    mockup_file_id = models.CharField(max_length=255, null=True)
    mockup_file_url = models.CharField(max_length=255, null=True)
    design_file_id = models.CharField(max_length=255, null=True)
    design_file_url = models.CharField(max_length=255, null=True)
    design_position = models.CharField(max_length=255, null=True)
    design_method = models.CharField(max_length=255, null=True)
    width_in = models.DecimalField(max_digits=16, decimal_places=2)
    height_in = models.DecimalField(max_digits=16, decimal_places=2)
    top_in = models.DecimalField(max_digits=16, decimal_places=2)
    left_in = models.DecimalField(max_digits=16, decimal_places=2)
    top_px = models.DecimalField(max_digits=16, decimal_places=2)
    left_px = models.DecimalField(max_digits=16, decimal_places=2)
    designed_obj_svg = models.TextField(blank=True, null=True)
    is_edited = models.BooleanField(null=False, default=False)
    is_default = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = 'order_item_designs'


class OrderAdjustment(TimeStamp):

    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=255, null=True)
    computation = models.CharField(max_length=255, null=True)
    adjustment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    display_description = models.TextField(null=True)
    creation_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'order_adjustments'


class OrderLineAdjustment(TimeStamp):

    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=255, null=True)
    computation = models.CharField(max_length=255, null=True)
    adjustment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    display_description = models.TextField(null=True)
    creation_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'order_line_adjustments'


class OrderLine(TimeStamp):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, default=0)
    tax_amount = models.DecimalField(max_digits=6, decimal_places=2)
    tax_currency = models.CharField(max_length=255, null=True)
    shipping_amount = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_currency = models.CharField(max_length=255, null=True)
    unit_price_amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit_price_currency = models.CharField(max_length=255, null=True)
    msrp_amount = models.DecimalField(max_digits=6, decimal_places=2)
    msrp_currency = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    total_line_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'order_lines'


class ShippingAddress(TimeStamp):

    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    map_key = models.CharField(max_length=255, null=True)
    geocode = models.CharField(max_length=255, null=True)
    street1 = models.CharField(max_length=255, null=True)
    street2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    pobox = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    postal_codetype = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'shipping_address'


class BillingAddress(TimeStamp):

    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    map_key = models.CharField(max_length=255, null=True)
    geocode = models.CharField(max_length=255, null=True)
    street1 = models.CharField(max_length=255, null=True)
    street2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    pobox = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    postal_codetype = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'billing_address'


class Currency(TimeStamp):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    currency_abbr = models.CharField(max_length=255, null=True)
    currency_name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'currencies'


class SavedItem(TimeStamp):

    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'saved_items'


class Security(TimeStamp):

    public_key = models.CharField(max_length=255, null=True)
    private_key = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Securities'


class Quotation(TimeStamp):

    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, default=None)
    email = models.EmailField(null=True)
    message = models.TextField()

    class Meta:
        db_table = 'quotation'


class UserArtwork(TimeStamp):

    ARTWORK_STATUS = (
        ('not-approved', 'not-approved'),
        ('approved', 'approved'),
    )

    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    order_item_id = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, null=True, blank=True, related_name='user_artwork')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    artwork = models.FileField(
        upload_to='user_artworks', null=True, verbose_name="")
    artwork_status = models.CharField(
        max_length=23, choices=ARTWORK_STATUS, default=ARTWORK_STATUS[1][0])

    class Meta:
        db_table = 'user_artwork'


class DiscountCoupon(TimeStamp):

    TYPE = (
        ('percentage', 'percentage'),
        ('flat', 'flat'),
    )

    coupon_code = models.CharField(max_length=255, null=True)
    type = models.CharField(
        max_length=23, choices=TYPE, default=TYPE[1][0])
    value = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'discount_coupon'

class OrderCommunication(TimeStamp):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_communication')
    order_item_id = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=15, null=True, blank=True)
    attachments = models.FileField(
        upload_to='order_activity_artwork', null=True, verbose_name="")


    class Meta:
        db_table = 'order_communication'


class OrderActivity(TimeStamp):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_activity')
    order_item_id = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    old_status = models.CharField(max_length=15, null=True, blank=True)
    new_status = models.CharField(max_length=15, null=True, blank=True)


    class Meta:
        db_table = 'order_activity'

class ArtworkProofing(TimeStamp):

    PROOF_STATUS = (
        ('received', 'received'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )

    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True, related_name='artwork_proofing')
    order_item_id = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, null=True, blank=True, related_name='artwork_proofing_item')
    attachments = models.FileField(
        upload_to='artwork_proofing', null=True, verbose_name="")
    status = models.CharField(
        max_length=23, choices=PROOF_STATUS, default=PROOF_STATUS[0][0])
    comment = models.TextField(null=True, blank=True)
    

    class Meta:
        db_table = 'artwork_proofing'

class SavedCards(TimeStamp):
    
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=True, blank=True)
    card_number = models.CharField(max_length=250, null=True, blank=True)
    expiry_date = models.CharField(max_length=250, null=True, blank=True)
    name_on_card = models.CharField(max_length=250, null=True, blank=True)
    

    class Meta:
        db_table = 'saved_cards'
