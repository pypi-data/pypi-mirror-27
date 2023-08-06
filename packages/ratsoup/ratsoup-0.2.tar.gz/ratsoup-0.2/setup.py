"""Rat soup package setup."""
from setuptools import setup


setup(
    name='ratsoup',
    packages=['ratsoup'],
    entry_points={
        'console_scripts': ['rats = ratsoup.rats:main']
    },
    version='0.2',
    description='Make soup for the rats',
    author='Paul Fablanod',
    author_email='p.fablanod@gmail.com',
    url='https://github.com/gabrielx52/ratsoup.git',
    download_url='https://github.com/gabrielx52/ratsoup/archive/0.2.tar.gz',
    keywords=['rat', 'rats', 'soup'],
    classifiers=[],
)
