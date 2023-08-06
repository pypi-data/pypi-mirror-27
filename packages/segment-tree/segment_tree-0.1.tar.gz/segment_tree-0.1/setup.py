from setuptools import setup
from setuptools import find_packages

setup(name='segment_tree',
      version='0.1',
      description='The most comprehensive implementation of Segment Tree.',
      url='https://github.com/evgeth/segment_tree',
      author='Evgeny Yurtaev',
      author_email='eugene@yurtaev.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      keywords='sample setuptools development',
      python_requires='>=3')
