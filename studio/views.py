from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import *
from django.db.models import Q
from .serializers import *

class StudioViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Studio.objects.filter(Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = StudioSerializer