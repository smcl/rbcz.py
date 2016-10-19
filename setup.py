from setuptools import setup

setup(
    name = 'rbcz',
    packages = [ 'rbcz', 'rbcz.test' ],
    version = '0.4',
    description = 'library for interacting with Czech Raiffeisen Bank\'s text bank statements',
    author = 'Sean McLemon',
    author_email = 'sean.mclemon@gmail.com',
    url = 'https://github.com/smcl/rbcz.py',
    download_url = 'https://github.com/smcl/rbcz.py/tarball/0.4',
    keywords = ['banking', 'raiffeisen', 'czech', 'cz'],
    classifiers = [],
    test_suite='rbcz.test.all',
    install_requires=[
        'unittest2'
    ],
    setup_requires=[
        'unittest2'
    ],
    
)
