import codecs
import os
import sys

try:
	from setuptools import setup
except:
	from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME ="imagetools" 

PACKAGES =["imagetools",]

DESCRIPTION ="This is a tool for image batch processing."

LONG_DESCRIPTION =read("README.txt")

KEYWORDS ="test python package"

AUTHOR ="zhaoxuhui"

AUTHOR_EMAIL ="zhaoxuhui@whu.edu.cn"

URL ="https://zhaoxuhui.top"

VERSION ="1.0.0"

LICENSE ="MIT"

setup(

    name =NAME,
    version =VERSION,
    description =DESCRIPTION,
    long_description =LONG_DESCRIPTION,
    classifiers =
	[

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',

        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

    ],
    keywords =KEYWORDS,
    author =AUTHOR,
    author_email =AUTHOR_EMAIL,
    url =URL,
    license =LICENSE,
    packages =PACKAGES,
    include_package_data=True,
    zip_safe=True,
)