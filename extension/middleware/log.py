import logging

from django.conf import settings
from django.db import connection
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):
    """日志中间件"""

    def process_request(self, request):
        try:
            logging.info("\n")
            logging.info(
                "************************************************* 下面是新的一条日志 ***************************************************"
            )
            logging.info("拦截请求的地址: %s；请求的方法: %s" % (request.path, request.method))
            logging.info(
                "==================================== headers 头信息 ===================================================="
            )
            logging.debug(
                f"HTTP_AUTHORIZATION: {request.META.get('HTTP_AUTHORIZATION')}"
            )
            # for key in request.META:
            #     if key[:5] == "HTTP_":
            #         logging.debug("%s %s" % (str(key), str(request.META[key])))
            logging.debug(f"Content-Type {request.META.get('CONTENT_TYPE')}")
            logging.info(
                "==================================== request body信息 =================================================="
            )
            logging.info(f"GET参数: {request.GET}")
            if request.content_type in (
                "application/json",
                "text/plain",
                "application/xml",
            ):
                if request.body:
                    logging.info(f"body参数: \n {request.body.decode()}")

            if request.content_type in (
                "multipart/form-data",
                "application/x-www-form-urlencoded",
            ):
                logging.info(f"body参数: \n {request.POST}")
        except Exception as e:
            logging.error("未知错误: %s" % str(e))
            return JsonResponse({"msg": "请求日志输出异常: %s" % e, "code": 1, "data": {}})

    def process_exception(self, request, exception):
        logging.error(
            "发生错误的请求地址: {}；错误原因: {}；错误详情: ".format(request.path, str(exception))
        )
        logging.exception(exception)
        return JsonResponse(
            {
                "msg": "An unexpected view error occurred: %s" % exception.__str__(),
                "code": 1,
                "data": {},
            }
        )

    def process_response(self, request, response):
        if settings.SHOWSQL:
            for sql in connection.queries:
                logging.debug(sql)
        return response
