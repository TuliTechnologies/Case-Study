from django.contrib import admin
from django.apps import apps

for model in apps.get_app_config('catalog_product').models.values():
    admin.site.register(model)