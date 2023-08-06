from setuptools import setup, find_packages
import os

#try:
#    import pypandoc
#
#    long_description = pypandoc.convert('README.md', 'rst')
#except(IOError, ImportError):
#    long_description = open('README.md').read()


_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

with open(os.path.join(_HERE, 'README.rst'),'w+') as fh:
    long_description = fh.read()



    long_description = long_description.replace("""<style scoped>
            .dataframe tbody tr th:only-of-type {
                vertical-align: middle;
            }

            .dataframe tbody tr th {
                vertical-align: top;
            }

            .dataframe thead th {
                text-align: right;
            }
        </style>""", "").replace("ipython2","python")
    fh.write(long_description)
    
    text_pypi = ''.join(fh.readlines()[:21])



    
    


setup(
    name = "json2df",
    version = "0.1.3.8",
    description = "convert json data to Pandas DataFrame",
    long_description = text_pypi,
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

