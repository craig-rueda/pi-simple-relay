import os

from setuptools import find_packages, setup

VERSION = "0.1.0"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name="pi_simple_relay",
    description=("PI Simple Relay Control"),
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pi_simple_relay = simple_relay.app:start',
        ],
    },
    install_requires=[
        "flask==2.3.3",
        "RPi.GPIO==0.7.1; sys_platform == 'linux'",
        "requests==2.24.0",
    ],
    author="Craig Rueda",
    author_email="craig@craigrueda.com",
    url="https://craigrueda.com",
    download_url="https://github.com/craig-rueda/pi-simple-relay",
    classifiers=["Programming Language :: Python :: 3.7"],
    tests_require=["nose>=1.0"],
    test_suite="nose.collector",
)
