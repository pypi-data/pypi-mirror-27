from setuptools import setup, find_packages

import os

_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

#try:
#    import pypandoc
#    long_description = pypandoc.convert('README.md', 'rst')
    
#except(IOError, ImportError):
#    long_description = open('README.md').read()



with open(os.path.join(_HERE, 'README.rst'),'r+') as fh:
    long_description = fh.read()

setup(
    name = "picutils",
    version = "0.1.6.8.5",
    description = "Hosting pictures into html, website, python Flask and GUI, image manupilation",
    long_description = long_description,
    author = "Shichao(Richard) Ji",
    author_email = "jshichao@vt.edu",
    url = "https://github.com/shichaoji/picutils",
    download_url = "https://github.com/shichaoji/picutils/archive/0.1.tar.gz",
    keywords = ['hosting','picture','image','python','flask'],
    license = 'MIT', 
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
    packages = find_packages(),
    install_requires=[
        'Pillow',
        'natsort',
      ]
)

