import json
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from extension.json_response_ext import JsonResponse


def handle_re_str(data: dict) -> str:
    """
    处理默认异常信息，将字典数据转换为字符串
    """
    finally_str = ""
    for key in data:  # 遍历字典
        res = "%s:" % key
        if isinstance(data[key], str):  # 如果是字符串，直接拼接
            finally_str += res + data[key]
        elif isinstance(data[key], list):  # 如果是列表，遍历列表
            for item in data[key]:
                if isinstance(item, str):  # 如果是字符串，直接拼接
                    res += item
                elif isinstance(item, dict):  # 如果是字典，递归调用
                    res += handle_re_str(item)
            finally_str += res
        else:
            finally_str += res
        finally_str += ";"
    return finally_str


def base_exception_handler(exc, context):
    """
    用于处理drf的异常定制返回，目的是统一返回信息，只有drf出现异常时才会执行，其他情况不执行
    """
    logging.error("DRF主动提示异常")
    error_msg = ["DRF主动提示异常"]
    response = exception_handler(exc, context)
    if response:  # 主要是用来处理字段验证的异常，将异常改为可读性更高的返回值
        error_msg.append("可处理的异常")
        logging.error("可处理的异常")
        logging.error(response.data)
        msg = ""
        new_data = json.loads(json.dumps(response.data))
        msg = handle_re_str(new_data)[:-2]
        code = 0 if response.status_code == 200 else 2
        return JsonResponse({"msg": msg, "code": code}, status=status.HTTP_200_OK).data
    logging.error("未处理的异常")
    logging.exception(exc)
    error_msg.append("未处理的异常")
    return JsonResponse({"msg": str(exc), "code": 1}, status=status.HTTP_200_OK).data
