import click
from datetime import datetime
from pathlib import Path
import logging
from scraper.webpages import BaseWebPage
from scraper.pipeline import scrape_webpages


logging.basicConfig(level=logging.INFO)

MAX_CONCURRENT_REQ = 2


def validate_max_days(ctx, param, value):
    del ctx
    del param
    if value <= 0:
        raise click.BadOptionUsage(
            "--max-days", "--max-days must be an integer larger than 0."
        )
    return value


@click.group()
def scraper_cli():
    pass


@scraper_cli.command()
@click.argument("filename", type=click.Path(), nargs=1)
@click.option(
    "--max-days",
    default=40,
    type=int,
    callback=validate_max_days,
    help="Scrape documents from n recent days. Default 40 days.",
)
def run_spiders(filename: Path, max_days: int) -> None:
    logging.info("Starting scraping process.")
    start = datetime.now()
    webpages = BaseWebPage.list_from_json(filename)
    if len(webpages) == 0:
        raise click.ClickException(f"No webpages found in the file {filename}.")
    scrape_webpages(webpages, MAX_CONCURRENT_REQ, max_days)
    end = datetime.now()
    logging.info(f"Scraping completed in {(end - start).seconds} seconds.")


if __name__ == "__main__":
    scraper_cli()
