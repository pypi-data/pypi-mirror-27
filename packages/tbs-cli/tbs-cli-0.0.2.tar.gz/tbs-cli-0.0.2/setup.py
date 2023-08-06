from setuptools import setup, find_packages

NAME = "tbs-cli"
VERSION = "0.0.2"
REQUIRES = ["click == 6.7", "tbs-sdk >= 0.0.1"]

setup(
    name=NAME,
    version=VERSION,
    description="3Blades Command Line Tool",
    author="John Griebel",
    author_email="jgriebel@3blades.io",
    url="https://github.com/3Blades/python-cli-tools",
    keywords=["3Blades", "Data Science"],
    packages=find_packages(),
    install_requires=REQUIRES,
    entry_points="""
        [console_scripts]
        tbs-cli=tbs:main
    """,
    include_package_data=True
)
