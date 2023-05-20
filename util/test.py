import unittest
from sensitive_filter_util import DFAFilter
from unittest.mock import MagicMock, patch

from util.jwt_token_util import JwtTokenUtil


class TestDFAFilter(unittest.TestCase):
    def setUp(self):
        self.filter = DFAFilter()

    def test_filter_message(self):
        filtered_message = self.filter.filter("这是一段包含敏感词的文本，敏感词应该被过滤。")
        self.assertEqual(filtered_message, "这是一段包含***的文本，***应该被过滤。")

    def test_filter_message_no_keywords(self):
        filtered_message = self.filter.filter("这是一段正常的文本。")
        self.assertEqual(filtered_message, "这是一段正常的文本。")

    def test_filter_message_with_replacement(self):
        filtered_message = self.filter.filter("这是一段包含敏感词的文本，敏感词应该被过滤。", repl="#")
        self.assertEqual(filtered_message, "这是一段包含###的文本，###应该被过滤。")
