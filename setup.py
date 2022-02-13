from setuptools import setup, find_packages

setup(
    name = 'FbGroupCrawler',
    packages = find_packages(),
    version = '1.0',
    description = 'Fb Group Crawler',
    author = '',
    author_email = '',
    url = 'https://github.com/asd2213857/FbGroupCrawler',
    download_url = '',
    keywords = [],
    classifiers = [],
    license='MIT',
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'pandas',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'FbGroupCrawler = FbGroupCrawler.__main__:main'
        ]
    }
)

