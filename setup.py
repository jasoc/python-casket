from setuptools import setup

with open("README.txt", 'r') as f:
    long_description = f.read()

setup(
   name='casket',
   version='0.1b1',
   license='GNU General Public License v3.0',
   description='A simple password manager written in Python',
   author='Jasoc',
   author_email='paridegiunta@gmail.com',
   packages=['Casket'],
   install_requires=['PyQt5'],
   include_package_data=True
)
