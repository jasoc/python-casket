from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='casket',
   version='0.1.b1',
   license='GNU General Public License v3.0',
   description='A simple password manager written in Python',
   author='giuntello',
   author_email='giuntello@protonmail.com',
   packages=find_packages(),
   install_requires=[
       'setuptools',
       'logzero',
       'cryptography',
       'passlib',
    ],
   include_package_data=True
)
