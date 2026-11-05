import unittest
from core.utils import valid_host
class HostValidationTests(unittest.TestCase):
    def test_valid_domain(self): self.assertTrue(valid_host('example.com'))
    def test_valid_ip(self): self.assertTrue(valid_host('127.0.0.1'))
    def test_invalid_host(self): self.assertFalse(valid_host('bad host'))
if __name__=='__main__': unittest.main()
