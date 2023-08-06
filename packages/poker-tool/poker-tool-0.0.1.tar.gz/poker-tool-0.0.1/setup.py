#!/usr/bin/env python3

from distutils.core import setup

setup(name='poker-tool',
      version='0.0.1',
      description='Rule based files collection and backup tool.',
      author='Chenyao2333',
      author_email='louchenyao@gmail.com',
      url='https://github.com/Chenyao2333/poker',
      scripts=["poker-cli"],
      packages = ["poker"],
      package_dir = {'poker': "poker"}
)
