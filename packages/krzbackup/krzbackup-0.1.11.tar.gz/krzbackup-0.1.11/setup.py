import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='krzbackup',
    packages=['krzbackup'],  # this must be the same as the name above
    version='0.1.11',
    description='A custom backuplibrary to coordinate multiple services',
    author='Kevin Honka',
    author_email='k.honka@krz-swd.de',
    license='GPLv3',
    url='http://git.mw-krz-swd.de/Meldewesen/Backup',  # use the URL to the github repo
    keywords=['Backup', 'Mysql', 'MariaDB', 'Elasticsearch', 'MongoDB'],  # arbitrary keywords
    classifiers=[],
    setup_requires=['pytest-runner'],
    install_requires=['requests'],
    tests_require=['pytest']
)
