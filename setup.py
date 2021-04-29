from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='uapy',
    version='1.0.1',
    author="Andres Castillo",
    author_email="indigohedgehog@gmail.com",
    description='Python wrapper for Linux UAPI ioctl',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/indigohedgehog/uapy",
    project_urls={
        "Bug Tracker": "https://github.com/indigohedgehog/uapy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux", "Topic :: Multimedia",
        "Topic :: Multimedia :: Video"
    ],
    install_requires=[
        'ctypes',
    ],    
    package_dir={"": "uapy"},
    packages=find_packages(where="uapy"),
    python_requires=">=3.6",
)