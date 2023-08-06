from setuptools import setup, find_packages

setup(
    name = "picutils",
    version = "0.1.5",
    description = "Hosting pictures into html, website, python Flask and GUI, image manupilation",
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

