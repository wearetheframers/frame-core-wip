from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(include=['frame*']),
    package_dir={'': 'src'}
)
