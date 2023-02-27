import logging

from django.conf import settings
from django.db import connection
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

"""
0 没有错误
1 未知错误  针对此错误  线上版前端弹出网络错误等公共错误
2 前端弹窗错误(包括：字段验证错误、自定义错误、账号或数据不存在、提示错误)
"""


class LogMiddleware(MiddlewareMixin):
    """日志中间件"""

    def process_request(self, request):
        try:
            logging.info(
                "************************************************* 下面是新的一条日志 ***************************************************"
            )
            logging.info("拦截请求的地址：%s；请求的方法：%s" % (request.path, request.method))
            logging.info(
                "==================================== headers 头信息 ===================================================="
            )
            for key in request.META:
                if key[:5] == "HTTP_":
                    logging.debug("%s %s" % (str(key), str(request.META[key])))
            logging.debug(f"Content-Type {request.META.get('CONTENT_TYPE')}")
            logging.info("代理IP：%s" % request.META.get("REMOTE_ADDR"))
            logging.info(
                "真实IP：%s" % request.META.get("HTTP_X_FORWARDED_FOR")
            )  # HTTP_X_REAL_IP
            logging.info(
                "==================================== request body信息 =================================================="
            )
            logging.info("params参数：%s" % request.GET)
            if request.content_type in (
                "application/json",
                "text/plain",
                "application/xml",
            ):
                if request.path not in ("/callpresell/",):
                    logging.info("body参数：\n %s" % request.body.decode())
            if request.content_type in (
                "multipart/form-data",
                "application/x-www-form-urlencoded",
            ):
                logging.info("是否存在文件类型数据：%s", bool(request.FILES))
                logging.info("data参数：%s", request.POST)
            logging.info(
                "================================== View视图函数内部信息 ================================================"
            )
            if request.method in {"DELETE", "delete"}:
                logging.info(f"{'>'*9} 发现删除数据 {'<'*9}")
                logging.info(f"删除请求的地址：{request.path}，执行用户：{request.user}")
        except Exception as e:
            logging.error("未知错误：%s" % str(e))
            return JsonResponse({"msg": "请求日志输出异常：%s" % e, "code": 1, "data": {}})

    def process_exception(self, request, exception):
        logging.error("发生错误的请求地址：{}；错误原因：{}；错误详情：".format(request.path, str(exception)))
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
