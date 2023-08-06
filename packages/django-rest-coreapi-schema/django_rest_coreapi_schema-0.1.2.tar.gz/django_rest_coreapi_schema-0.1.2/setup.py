from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_rest_coreapi_schema',
    version='0.1.2',
    description='Django restframework custom schema',
    long_description=long_description,
    url='https://github.com/emilioag/django_rest_coreapi_schema',
    author='The Python Packaging Authority',
    author_email='agonzalez.emilio@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django restframework schema coreapi swagger',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=[
        'Django==2.0',
        'djangorestframework==3.7.7',
        'coreapi==2.3.3',
        'Pygments==2.2.0',
        'Markdown==2.6.10',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)