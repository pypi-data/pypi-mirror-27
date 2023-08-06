import unittest
try:
    from unittest import patch
except ImportError:
    from mock import patch


class TestMain(unittest.TestCase):
    def test_main_import(self):
        from ethproxy import main

    def test_cli_import(self):
        from ethproxy import cli
