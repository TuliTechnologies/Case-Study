from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *


class StudioSerializer(ModelSerializer):

    class Meta:
        model = Studio
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
