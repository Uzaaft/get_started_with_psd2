#!/usr/bin/env python3

from setuptools import find_packages, setup

install_requires = [
    "requests==2.25.1",
    "selenium==3.141.0",
]


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dnb_psd2",
    version="0.0.1a",
    author="Njord Technologies",
    author_email="post@njordtechnologies.com",
    url="https://github.com/Njord-Technologies/get_started_with_psd2",
    packages=find_packages(),
    install_requires=install_requires,
    description="Get started with the DNB PSD2 API. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/Njord-Technologies/get_started_with_psd2/archive/master.zip",
    keywords=["dnb psd2", "open banking"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
