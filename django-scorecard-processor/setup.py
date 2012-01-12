from setuptools import setup, find_packages
import os
import platform

DESCRIPTION = "A Django reusable application for collecting data and transforming it into scorecards"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

setup(
    name='django-scorecard-processor',
    version='0.1',
    packages=['scorecard_processor'],
    author='Bradley Whittington',
    author_email='radbrad182@gmail.com',
    url='http://github.com/bradwhittington/django-scorecard-processor/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    install_requires=['django-cerial','django-grapelli','south','django-bootstrap','tablib','xlrd','xlwt'],
    classifiers=CLASSIFIERS,
)

