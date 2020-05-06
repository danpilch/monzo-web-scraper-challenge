#!/usr/bin/env python

from scraper.webcrawler import Crawler
import argparse
import logging


def main():
    """ Create a cli argparser """
    parser = argparse.ArgumentParser(
        "a simple web crawler"
    )

    parser.add_argument(
        "--url",
        "-u",
        help="Root URL to start crawling from",
        default="https://monzo.com"
    )
    
    parser.add_argument(
        "--log",
        "-l",
        dest="logLevel",
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level"
    )

    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(
                format='%(asctime)s %(message)s',
                level=getattr(logging, args.logLevel)
        )

    """ Start crawler """
    crawl = Crawler(
        args.url
    )

    crawl.start()


if __name__ == "__main__":
    main()

