from setuptools import setup, find_packages

setup(
    name="vint_train",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"vint_train.data": ["*.yaml"]},
)
