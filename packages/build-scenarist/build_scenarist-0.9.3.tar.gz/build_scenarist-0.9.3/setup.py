# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re

# from scenarist import version

def read(*names, **kwargs):
      with io.open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
            return fp.read()

def find_version(*file_paths):
      version_file = read(*file_paths)
      version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
      if version_match:
            return version_match.group(1)
      raise RuntimeError("Unable to find version string.")

setup(name='build_scenarist',
      version=find_version("build_scenarist", "__init__.py"),
      description='',
      url='http://github.com/sogimu/scenarist',
      author='Aleksandr Lizin',
      author_email='sogimu@nxt.ru',
      license='MIT',
      packages=['build_scenarist'],
      scripts=['scenarist.py'],
      package_data={'build_scenarist': ['src/*']},
      zip_safe=True)
