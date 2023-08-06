from setuptools import setup, find_packages
import os


_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

with open(os.path.join(_HERE, 'README.rst'),'r') as fh:
    text = fh.read()

setup(
    name = "json2df",
    version = "0.1.3.3",
    description = "convert json data to Pandas DataFrame",
    long_description = text,
    author = "Shichao(Richard) Ji",
    author_email = "jshichao@vt.edu",
    url = "https://github.com/shichaoji/json2df",
    download_url = "https://github.com/shichaoji/json2df/archive/0.1.1.tar.gz",
    license = 'MIT',
    keywords = ['data','json','dataframe','python'],
    classifiers = [
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 2', 
	'Programming Language :: Python :: 3',
	],
    packages = find_packages(),
    install_requires=[
          'pandas',
      ]
)

