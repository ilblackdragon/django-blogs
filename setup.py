#!/usr/bin/python

import os
from setuptools import setup, find_packages

from blog import VERSION, PROJECT


MODULE_NAME = 'django-blogs'
PACKAGE_DATA = list()

for directory in [ 'blog/templates', 'blog/static' ]:
    for root, dirs, files in os.walk( os.path.join( MODULE_NAME, directory )):
        for filename in files:
            PACKAGE_DATA.append("%s/%s" % ( root[len(MODULE_NAME)+1:], filename ))


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

    install_requires = [ 'django>=1.2', 
                         'django-misc', 
                         'django-pagination', 
                         'django-tagging', 
                         'django-voter',
                       ],
)

if __name__ == "__main__":
    setup( **META_DATA )

