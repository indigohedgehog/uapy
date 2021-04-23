from setuptools import find_packages, setup

setup(
    name = 'uapy',
    version = '0.2.0',
    packages = find_packages('uapy'),
    install_requires = [''],
    entry_points = {
        'uapy.api': [
            'uapy=uapy.api:main'
        ]
    }
)