from setuptools import setup

current_version = '0.6'

# convert from github markdown to rst
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'rbcz',
    packages = [ 'rbcz', 'rbcz.test' ],
    version = current_version,
    description = 'library for interacting with Czech Raiffeisen Bank\'s text bank statements',
    author = 'Sean McLemon',
    author_email = 'sean.mclemon@gmail.com',
    url = 'https://github.com/smcl/rbcz.py',
    download_url = 'https://github.com/smcl/rbcz.py/tarball/%s' % (current_version),
    keywords = ['banking', 'raiffeisen', 'czech', 'cz'],
    classifiers = [],
    test_suite='rbcz.test.all',
    install_requires=[
        'unittest2'
    ],
    setup_requires=[
        'unittest2'
    ],
    long_description=long_description
)
