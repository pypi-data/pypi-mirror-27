#  -*- coding: utf-8 -*-
"""
Setuptools script for the md-mqtt project.
"""
import os

try:
    from setuptools import setup, find_packages
    from setuptools.command.build_py import build_py
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.build_py import build_py


def required(fname):
    return open(
        os.path.join(
            os.path.dirname(__file__), fname
        )
    ).read().split('\n')


setup(
    name="md-mqtt",
    version="0.0.1",
    packages=find_packages(),
    scripts=[],
    entry_points={
        "console_scripts": [
            "md_mqtt = md_mqtt.__main__:main"
        ]
    },
    include_package_data=True,
    setup_requires='pytest-runner',
    tests_require='pytest',
    install_requires=required('requirements.txt'),
    test_suite='pytest',
    zip_safe=False,
    # Metadata for upload to PyPI
    author='Ellis Percival',
    author_email="md_mqtt@failcode.co.uk",
    description="Publish Linux MD RAID status to MQTT",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Communications",
        "Topic :: Home Automation",
        "Topic :: System :: Networking"
    ],
    license="MIT",
    keywords="",
    url="https://github.com/flyte/md-mqtt"
)
