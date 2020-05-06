#!/usr/bin/env python
import logging
import requests
import tldextract
import concurrent.futures
from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
import pprint


class Crawler(object):
    def __init__(self, base_url):
        self.base_url = base_url

        # Get the registered domain
        self.base_domain = tldextract.extract(
            self.base_url
        ).registered_domain
        
        # Concurrent workers
        self.max_workers = 8 
        
        # Create a defaultdict of type list to store crawling data
        self.site_map = defaultdict(list)

    def http_request(self, url):
        """ Perform a HTTP request and return page body """
        logging.debug(f"Performing http_request for: {url}")
        try:
            response = requests.get(url)
            return response.content
        except Exception as e:
            logging.error(f"Error: {e}")
            raise 
        
    def relative_url(self, item):
        try:
            return urljoin(self.base_url, item)
        except Exception as e:
            return None

    def find_external_links(self, link):
        """ Check if current link is part of root domain and check there is no subdomain, return bool"""
        return (tldextract.extract(link).registered_domain == self.base_domain and tldextract.extract(link).subdomain == '') 

    def link_parser(self, page_body):
        """ find links in html, fix up relative links and remove any 
            links not associated with root domain
        """
        # Extract all href links from a html doc and store in list
        try:
            raw_links = []
            for link in BeautifulSoup(page_body, parse_only=SoupStrainer('a'), features="html.parser"):
                # Check link has href attr
                if link.has_attr('href'):
                    # Check any relative links that might cause a loop
                    if link['href'] not in {'#', '/'}:
                        raw_links.append(link['href'])

            # Check if links are relative, if they are assume they're part of root and rewrite
            reative_checked_links = [self.relative_url(link) if link.startswith('/') else link for link in raw_links]
            
            # Remove links that aren't associated with root and return
            return [link for link in reative_checked_links if self.find_external_links(link)]
        except Exception as e:
            raise

    def concurrent_process(self, url):
        try:
            # here we're using a threadpoolexecutor to concurrently make http requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_get_url = {executor.submit(self.http_request, u): u for u in self.site_map[url]}
                for future in concurrent.futures.as_completed(future_get_url):
                    current_url = future_get_url[future]
                    current_page = future.result()
                    # Check if we have already seen this page before (dict key)
                    # if we haven't lets scrape the page for links
                    if current_url not in self.site_map:
                        subpage_links = self.link_parser(current_page)
                        self.site_map[current_url] = subpage_links
        except Exception as e:
            raise

    def start(self):
        # Get root html doc
        self.base_body = self.http_request(self.base_url)
        # Find all links in root
        root_links = self.link_parser(self.base_body)
        # Add root domain and link data to dict
        self.site_map[self.base_url] = root_links

        # Iterate over root links and then find links on their pages that haven't been found before
        self.concurrent_process(self.base_url)

        #TODO: we could go deeper and iterate over the next batch of links, but haven't implemented 
        # due to time constraints

        # Output results
        pprint.pprint(self.site_map)
