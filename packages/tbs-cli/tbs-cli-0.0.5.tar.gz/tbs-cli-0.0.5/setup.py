from setuptools import setup, find_packages

NAME = "tbs-cli"
VERSION = "0.0.5"
REQUIRES = ["click == 6.7", "tbs-sdk >= 0.0.1"]

setup(
    name=NAME,
    version=VERSION,
    description="3Blades Command Line Tool",
    author="John Griebel",
    author_email="jgriebel@3blades.io",
    url="https://github.com/3Blades/python-cli-tools",
    download_url = 'https://github.com/3Blades/python-cli-tools/archive/0.0.3.tar.gz',
    keywords=["3Blades", "Data Science"],
    packages=["command_groups", "tbscli"],
    install_requires=REQUIRES,
    entry_points={'console_scripts': ["tbs=tbscli.tbs:main"]},
    include_package_data=True,
    license="BSD 3-clause"
)
