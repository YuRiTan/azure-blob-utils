import pathlib
from setuptools import setup, find_packages

root_dir = pathlib.Path(__file__).parent
README = (root_dir / "README.md").read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='azure-blob-utils',
    version='0.0.1',
    url='https://github.com/YuRiTan/azure-blob-utils',
    description='Some Azure blob storage utils.',
    long_description=README,
    long_description_content_type='text/markdown',
    author="Yu Ri Tan",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires=requirements,
    packages=find_packages(exclude=('tests',)),
)

