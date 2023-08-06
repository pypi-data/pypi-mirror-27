from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-core-waili',
    version='0.1.3.dev1',
    description='Django tools',
    long_description=long_description,
    url='https://github.com/linxuedong/django-core-waili',  # Optional
    author='linxuedong',
    author_email='xuedonglin1994@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    keywords='django tools',
    packages=find_packages(exclude=['core',]),
)
