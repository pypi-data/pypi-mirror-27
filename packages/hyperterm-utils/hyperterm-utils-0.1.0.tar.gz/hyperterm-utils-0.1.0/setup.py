from setuptools import setup, find_packages

setup(name='hyperterm-utils',
      version='0.1.0',
      description="Python build tools and utilities for Hyperterm",
      url='https://github.com/mikeanthonywild/hyperterm-utils',
      author='Mike Wild',
      author_email='mike@mikeanthonywild.com',
      license='MIT',
      packages=find_packages(),
      long_description=open('README.md').read(),
      include_package_data=True,
      install_requires=[])
