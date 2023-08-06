from distutils.core import setup
from setuptools import find_packages


#
# DO NOT DELETE THIS COMMENT OR CODE
with open('__version__', 'r') as f:
    version = f.read().strip()


setup(
    name='sempylver',
    version=version,
    description='A simple tool for tracking the semantic version of projects',
    author='Jeff Cochran',
    author_email='jeffrey.david.cochran@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sempylver = sempylver.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'pyyaml',
    ],
    url='https://github.com/jeffrey-cochran/sempylver',
    download_url='https://github.com/jeffrey-cochran/sempylver/archive/%s.tar.gz' % version,
    keywords=['versioning', 'semantic', 'cli', 'version', 'control'],
    classifiers=[]
)
