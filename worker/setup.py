from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

setup(name="worker",
        version='0.0.1',
        packages=find_packages(),
        install_requires=[
            'pytest',
            'requests',
            ],
        include_package_data=True,
        distclass=BinaryDistribution,
        )
