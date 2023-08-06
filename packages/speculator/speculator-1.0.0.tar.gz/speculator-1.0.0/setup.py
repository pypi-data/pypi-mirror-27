from setuptools import setup, find_packages
from codecs import open
from os import path

if path.exists('README.rst'):
    readme = open('README.rst').read()
elif path.exists('README.md'):
    readme = open('README.md').read()
else:
    readme = 'Failed to upload!'

"""
try:
    import pypandoc
    readme = pypandoc.convert(readme_path, 'rst')
except (IOError, ImportError):
    readme = open(readme_path).read()
"""

setup(
    name='speculator',
    version='1.0.0',
    description='Speculator predicts the price trend of cryptocurrencies like Bitcoin and Ethereum with machine learning models and technical analysis.',
    long_description=readme,
    url='https://github.com/amicks/Speculator',
    download_url='https://github.com/amicks/Speculator/archive/1.0.0.tar.gz',
    author='Allston Mickey',
    author_email='allston.mickey@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=[
        'finance',
        'price',
        'trend',
        'analysis',
        'machine learning',
        'artificial intelligence',
        'bitcoin',
        'ethereum',
        'cryptocurrency',
        'crypto',
        'api',
        'REST',
        'web'
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'delorean',
        'requests',
        'numpy',
        'scikit-learn',
        'tensorflow',
        'pandas',
        'flask',
        'flask-cache',
        'flask-restful',
        'webargs'
    ]
)
