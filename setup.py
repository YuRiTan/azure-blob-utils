from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='azure-blob-utils',
      url='https://github.com/YuRiTan/azure-blob-utils',
      version='0.0.1',
      description='Some Azure blob storage utils.',
      install_requires=requirements,
      packages=find_packages(),
      zip_safe=False)

