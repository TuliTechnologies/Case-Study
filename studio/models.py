from django.db import models
from pages.models import TimeStamp
from accounts.models import Users

class Studio(TimeStamp):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
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
        super(Studio, self).save()

    class Meta:
        db_table = 'studio'