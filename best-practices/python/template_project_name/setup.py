from setuptools import find_packages
from distutils.core import setup

# print(find_packages( include=['template_project_name']))

INSTALL_REQUIRES = ["matplotlib"]

setup(
    name="template_project_name",
    version="0.0.1",
    author="Jonas Frey",
    author_email="jonfrey@ethz.ch",
    packages=find_packages(),
    python_requires=">=3.6",
    description="A small example package",
    install_requires=[],
)
