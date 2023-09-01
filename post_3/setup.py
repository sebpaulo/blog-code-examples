from setuptools import setup, find_packages


setup(
    name='scraper',
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        scraper_cli=cli.run:scraper_cli
    '''
)