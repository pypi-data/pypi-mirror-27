# coding=utf-8

from setuptools import setup, find_packages
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs if ir.req]

setup(
    name='pocoui',
    version='1.0.5',
    keywords="poco",
    description='Poco cross-engine UI automated test framework.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    license='Apache License 2.0',
    author='adolli',
    author_email='adolli@163.com',
)
