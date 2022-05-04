from setuptools import find_packages
from distutils.core import setup

setup(
    name="template_project_name",
    version="0.0.1",
    author="Jonas Frey",
    author_email="jonfrey@ethz.ch",
    packages=find_packages(),
    python_requires=">=3.6",
    description="A small example package",
    install_requires=["opencv-python","neptune-client", "matplotlib", "numpy", "imageio", "pillow", "scikit-image", "pyyaml", "pytorch-lightning"],
)
