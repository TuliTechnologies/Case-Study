from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                return self.num_pages
            else:
                raise

class CustomPaginationResponse(PageNumberPagination):
    django_paginator_class = SafePaginator
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'current_page': self.page.number,
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'per_page': self.page.paginator.per_page,
            'results': data
        })
