import logging
from click.testing import CliRunner
from cli.run import run_spiders


def test_scraper_cli(webpages_filepath, caplog):
    with caplog.at_level(logging.INFO):
        runner = CliRunner()
        result = runner.invoke(run_spiders, [webpages_filepath, "--max-days", 50])
        assert result.exit_code == 0
        assert "Starting scraping process." in caplog.text
        assert "Added document" in caplog.text
        assert "Scraping completed" in caplog.text