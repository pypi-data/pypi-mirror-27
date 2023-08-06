from setuptools import setup
from setuptools import find_packages

numerapi_version = '0.6.0'

setup(
    name="numerapi",
    version=numerapi_version,
    maintainer="uuazed",
    maintainer_email="uuazed@gmail.com",
    description="Automatically download and upload data for the Numerai machine learning competition",
    url='https://github.com/uuazed/numerapi',
    platforms="OS Independent",
    license='MIT License',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "requests",
    ]
)
