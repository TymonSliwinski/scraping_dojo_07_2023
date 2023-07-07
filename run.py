"""
Main file to run the scraper, scrapes data from website specified in INPUT_URL, 
and saves to file specified in OUTPUT_FILE in JSON format.
"""

import logging
from constants import PROXY, INPUT_URL, OUTPUT_FILE
from scraper import Scraper
from output import JSONOutput

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def main():
    try:
        scraper = Scraper(PROXY, INPUT_URL, output=JSONOutput(OUTPUT_FILE))
        scraper.scrape()
    except Exception as e:
        logger.error('Error: %s', e)


if __name__ == '__main__':
    main()
