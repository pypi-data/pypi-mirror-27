# Useful doc: http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html
from distutils.core import setup

setup(
    name='HerosRPG',
    version='1.2',
    packages=['HerosRPG'],
    url='',
    license='LICENSE.txt',
    author='ianc',
    author_email='ianc@slalom.com',
    description='A simple console based  Role Playing Game in Python',
    long_description=open('README.txt').read()
)
