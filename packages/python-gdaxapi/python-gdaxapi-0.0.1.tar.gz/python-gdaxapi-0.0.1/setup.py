import pypandoc as pd
from setuptools import setup, find_packages

__version__ = None
with open('gdax/version.py') as f:
    exec(f.read())

setup(
    name='python-gdaxapi',
    version=str(__version__),
    author='Jay Hale',
    author_email='jay@jtst.io',
    url='https://github.com/jtstio/python-gdaxapi',
    packages=find_packages(),
    license='MIT',
    description='GDAX API wrapper for Python',
    long_description=pd.convert(
        open('./README.md').read(),
        'rst',
        format='md'),
    install_requires=('requests >= 2.18, < 3'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[
        'gdax',
        'gdax-api',
        'bitcoin', 
        'ethereum',
        'litecoin',
        'BTC',
        'ETH',
        'LTC',
        'client',
        'api',
        'wrapper',
        'currency',
        'trading',
        'trading-api',
        'coinbase'
    ],
)