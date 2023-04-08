from setuptools import setup

with open("./README.md") as f:
    long_description = f.read()

with open("./requirements.txt") as fp:
    dependencies = [line.strip() for line in fp.readlines()]

setup(
    name="MLOps stock prediction service",
    version="0.1.0",
    description="MLOps demo",
    long_description=long_description,
    author="Lucas LE RAY",
    packages=["src"],
    install_requires=dependencies,
)
