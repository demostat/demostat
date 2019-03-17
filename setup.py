import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import demostat

setup(
    name='demostat',
    version=demostat.version,
    packages=find_packages(),
    include_package_data=True,
    license='', # We dont have a lincense at this time
    description='Status page for scheduled political demonstrations',
    long_description=README,
    url='https://demostat.de/',
    author='The Demostat Community',
    author_email='hallo@demostat.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.6",
    install_requires=[
        'Django>=2.1',
    ],
)
