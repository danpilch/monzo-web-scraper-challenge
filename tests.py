import unittest
from scraper.webcrawler import Crawler


class CrawlerTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler('https://monzo.com')

    def test_http_request(self):
        self.assertEqual(self.crawler.http_request('https://postman-echo.com/status/200'), b'{"status":200}')

    def test_relative_url(self):
        self.assertEqual(self.crawler.relative_url('/test'), 'https://monzo.com/test')

    def test_find_external_links(self):
        self.assertTrue(self.crawler.find_external_links('http://monzo.com/test'), True)
        self.assertFalse(self.crawler.find_external_links('http://bbc.co.uk/test'), False)

    def test_link_parser(self):
        invalid_url = "https://www.w3schools.com/html/"
        valid_url = "https://monzo.com/test"
        page_body = """<!DOCTYPE html><html><body><h2>HTML Links</h2><p><a href="{0}">Visit our HTML tutorial</a></p></body></html>"""

        self.assertEqual(self.crawler.link_parser(page_body.format(invalid_url)), [])
        self.assertEqual(self.crawler.link_parser(page_body.format(valid_url)), [valid_url])


def suite():
    return unittest.TestSuite([
        CrawlerTest['test_http_request'],
        CrawlerTest['test_relative_url'],
        CrawlerTest['test_find_external_links'],
        CrawlerTest['test_link_parser'],
    ])
