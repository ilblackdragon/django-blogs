#!/usr/bin/python

import os
from setuptools import setup, find_packages

from blog import VERSION, PROJECT


MODULE_NAME = 'django-blogs'
PACKAGE_NAME = 'blog'
PACKAGE_DATA = list()

for directory in [ 'templates', 'static', 'locale' ]:
    for root, dirs, files in os.walk( os.path.join( PACKAGE_NAME, directory )):
        for filename in files:
            PACKAGE_DATA.append("%s/%s" % ( root[len(PACKAGE_NAME)+1:], filename ))


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name = PROJECT,
    version = VERSION,
    description = read('DESCRIPTION'),
    long_description = read('README.rst'),
    license='MIT',

    author = "Illia Polosukhin",
    author_email = "ilblackdragon@gmail.com",

    url = "http://github.com/ilblackdragon/django-blogs.git",

    packages = find_packages(),
    package_data = { '': PACKAGE_DATA, },

    dependency_links = [
                         'https://github.com/ProstoKSI/html-cleaner/archive/master.zip#egg=html-cleaner',
                       ],
    install_requires = [ 'django>=1.2',
                         'pytils',
                         'django-misc', 
                         'django-pagination', 
                         'django-tagging', 
                         'html-cleaner',
                       ],
)

if __name__ == "__main__":
    setup( **META_DATA )

