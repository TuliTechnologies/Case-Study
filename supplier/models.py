from django.db import models
from pages.models import TimeStamp
from accounts.models import Users

class Supplier(TimeStamp):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True) 
    first_name  = models.CharField(max_length=255, null=True)
    last_name  = models.CharField(max_length=255, null=True)
    email  = models.CharField(max_length=255, null=True)
    phone  = models.CharField(max_length=255, null=True)
    verified_email  = models.BooleanField(default=False)
    gender  = models.CharField(max_length=255, null=True)
    date_of_birth  = models.DateField(null=True, blank=True)
    notes  = models.CharField(max_length=255, null=True)
    rating  = models.CharField(max_length=255, null=True) # need to go some R&D on this

    def save(self, **kwargs):
        super(Supplier, self).save()

    class Meta:
        db_table = 'supplier'

class SupplierAddress(TimeStamp):
    supplier_id  = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    address1  = models.TextField(null=True, blank=True)
    address2  = models.TextField(null=True, blank=True)
    zip  = models.CharField(max_length=255, null=True)
    city  = models.CharField(max_length=255, null=True)
    province  = models.CharField(max_length=255, null=True)
    province_code  = models.CharField(max_length=255, null=True)
    country  = models.CharField(max_length=255, null=True)
    country_code  = models.CharField(max_length=255, null=True)

    def save(self, **kwargs):
        super(SupplierAddress, self).save()

    class Meta:
        db_table = 'supplier_addresses'
