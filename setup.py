import os, sys
from distutils.core import setup

def read(fname):
   return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
   # metadata
   name='psyncopath',
   description='Tool for synchronizing directories by using rsync',
   long_description=read('README'),
   license='MIT',
   version='1.01',
   author='Romain Picard',
   author_email='romain.picard@oakbits.com',
   url='https://github.com/MainRo/psyncopath',
   classifiers = [
      'Topic :: System :: Archiving',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2'],

   packages=['psyncopathlib'],

   scripts=['scripts/psyncopath'],
)
