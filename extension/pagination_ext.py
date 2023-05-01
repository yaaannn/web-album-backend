import logging
from django.conf import settings
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from extension.json_response_ext import JsonResponse


class Pagination(PageNumberPagination):
    """自定义分页类"""

    page_size = 2
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100

    def get_my_next(self):
        # logging.info("{}-{}".format(8888, self.request.path))
        # logging.info("{}-{}".format(8888, settings.SERVER_NAME))
        # logging.info("{}-{}".format(8888, self.get_next_link().split(self.request.path)))
        return (
            settings.SERVER_NAME
            + self.request.path
            + self.get_next_link().split(self.request.path)[1]
        )

    def get_my_pre(self):
        return (
            settings.SERVER_NAME
            + self.request.path
            + self.get_previous_link().split(self.request.path)[1]
        )

    def get_paginated_response(self, data):
        return JsonResponse(
            {
                "total": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        ).data

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "total": {
                    "type": "integer",
                    "example": 123,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "data": schema,
            },
        }
