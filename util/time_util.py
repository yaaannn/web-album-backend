import time
import logging
from datetime import datetime


class TimeUtil:
    """
    自定义时间处理工具类
    """

    @staticmethod
    def timestamp_str(timestamp: int, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        时间戳转时间字符串
        :param timestamp: 时间戳
        :param format: 时间格式
        :return: 时间字符串
        """
        try:
            if not isinstance(timestamp, int):
                raise ValueError("timestamp 应为 int 类型")
            return datetime.fromtimestamp(timestamp).strftime(format)
        except Exception as e:
            logging.error(str(e))
            raise e

    @staticmethod
    def str_timestamp(time_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> int:
        """
        时间字符串转时间戳
        :param time_str: 时间字符串
        :param format: 时间格式
        :return: 时间戳
        """
        try:
            if not isinstance(time_str, str):
                raise ValueError("time_str 应为 str 类型")
            return int(datetime.strptime(time_str, format).timestamp())
        except Exception as e:
            logging.error(str(e))
            raise e

    @staticmethod
    def datetime_timestamp(date_time: datetime) -> int:
        """
        datetime转时间戳
        :param date_time: datetime
        :return: 时间戳
        """
        try:
            if not isinstance(date_time, datetime):
                raise ValueError("datetime 应为 datetime 类型")
            return int(date_time.timestamp())
        except Exception as e:
            logging.error(str(e))
            raise e


if __name__ == "__main__":
    print(TimeUtil.timestamp_str(1600000000))
    print(TimeUtil.str_timestamp("2020-09-14 10:40:00"))
    print(TimeUtil.datetime_timestamp(datetime.now()))
    print(datetime.now().timestamp())
