from setuptools import setup
from setuptools import find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(name='npr',
      version='1.2.1',
      description='NPR cloud framework',
      long_description='Self-authenticating module for accessing NPR APIs in Python.',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
      ],
      url='http://github.com/perrydc/npr',
      author='Demian Perry',
      author_email='dperry@npr.org',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      keywords='public, radio, stream, metadata, api, service, npr',
      python_requires='>=3')
