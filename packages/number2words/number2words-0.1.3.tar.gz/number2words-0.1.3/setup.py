import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='number2words',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Number2Words converts numbers to words according to Indian Numbering System.',
    long_description=README,
    author='hchockarprasad',
    author_email='hchockarprasad@gmail.com',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
)
