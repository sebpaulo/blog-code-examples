from collections.abc import Sequence
from datetime import datetime, timedelta
import concurrent.futures
from functools import partial
from pydantic import ValidationError
import logging
from scraper.dispatch import run_spider
from scraper.documents import Document
from scraper.webpages import BaseWebPage


def insert_doc_to_db(document: Document) -> None:
    # code for DB insertion would go here
    logging.info(f"\nAdded document:\n{document}\n")


def add_documents(wp: BaseWebPage, max_days: int) -> None:
    for item in run_spider(wp):
        try:
            document = Document(**item._asdict())
            if max_days and datetime.combine(
                document.publication_date, datetime.min.time()
            ) < (datetime.now() - timedelta(days=max_days)):
                break
            insert_doc_to_db(document)
        except ValidationError:
            logging.error("Skipping document with invalid data.")
            continue


def scrape_webpages(
    wp_list: Sequence[BaseWebPage], max_conc_req: int, max_days: int
) -> None:
    max_workers = min(max_conc_req, len(wp_list))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(partial(add_documents, max_days=max_days), wp_list)
