# Imports
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'livestock_linux\README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='livestock_linux',
      version='0.0.1.dev14',
      description='Livestock is a plugin/library for Grasshopper written in Python',
      long_description=long_description,
      url='https://github.com/ocni-dtu/livestock_gh',
      author='Christian Kongsgaard Nielsen',
      author_email='ocni@dtu.dk',
      license='MIT',
      classifiers=[
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: Professionals and students',
                   'Topic :: Environmental Analysis',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6',
                  ],
      keywords='hydrology 3dmodeling grasshopper',
      packages=['livestock_linux'],
      install_requires=['numpy'],
      python_requires='>=3',
      entry_points={'console_scripts': ['livestock_linux=livestock_linux:main',],},
      )
