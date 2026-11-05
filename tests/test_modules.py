import unittest
from urllib.parse import urlparse
class URLParsingTests(unittest.TestCase):
    def test_https_url(self):
        parsed=urlparse('https://example.com/path')
        self.assertEqual(parsed.scheme,'https')
        self.assertEqual(parsed.hostname,'example.com')
if __name__=='__main__': unittest.main()
