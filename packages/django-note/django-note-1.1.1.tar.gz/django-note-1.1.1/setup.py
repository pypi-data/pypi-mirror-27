import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-note',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django==1.11.6',
    ],
    license='GPL-3.0',
    description='A simple Django app to conduct Web-based note lists.',
    long_description=README,
    url='https://www.example.com/',
    author='Skochinskyi Dmytro',
    author_email='skodmy@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
