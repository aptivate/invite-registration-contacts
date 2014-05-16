import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
LICENSE = open(os.path.join(os.path.dirname(__file__), 'LICENSE')).read()
DESCRIPTION = ("A companion app to invite-registration for basic management"
               "of users outside of Django's admin interface")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='invite-registration-contacts',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=README,
    url='https://github.com/aptivate/invite-registration-contacts',
    author='Marko Samastur',
    author_email='markos@aptivate.org',
    install_requires=['django>=1.5', 'invite-registration'],
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Topic :: Internet :: WWW/HTTP',
                'Topic :: Internet :: WWW/HTTP :: Dynamic Content'],
)
