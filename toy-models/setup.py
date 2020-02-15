from setuptools import setup, find_packages


setup(
    name="toy-models",
    packages=find_packages(include=["project", "project.*"]),
)