from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

setup(name="master",
        version='0.0.1',
        packages=find_packages(),
        install_requires=[
            'pytest',
            'requests',
#            'validators',
#            'pyyaml',
            'requests[socks]',
#            'varname',
            'urllib3[socks]',
            'flask',
            'waitress',
#            'json',
#            'flask_restful'
            ],
        include_package_data=True,
        distclass=BinaryDistribution,
        )

