import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read("README.md") if os.path.isfile("README.md") else ""

setup(
    name="polygon-etl",
    version="0.1.9",
    author="Evgeny Medvedev",
    author_email="evge.medvedev@gmail.com",
    description="Tools for exporting Polygon blockchain data to CSV or JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blockchain-etl/polygon-etl",
    packages=find_packages(exclude=["schemas", "tests"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="polygon",
    # web3.py doesn't work on 3.5.2 and less (https://github.com/ethereum/web3.py/issues/1012)
    # google-cloud-pubsub==2.1.0 requires >=3.6 (https://pypi.org/project/google-cloud-pubsub/2.1.0/)
    # collections.Mapping unsupported in 3.10 (https://bugs.python.org/issue44737)
    python_requires=">=3.6,<3.10",
    install_requires=[
        "base58",
        "blockchain-etl-common==1.6.1",
        "click==7.0",
        "eth-abi==1.3.0",
        "eth-utils==1.8.4",
        "ethereum-dasm==0.1.4",
        "requests",
        "web3==4.7.2",
    ],
    extras_require={
        "streaming": [
            "google-cloud-pubsub==2.1.0",
            "google-cloud-storage==1.33.0",
            "pg8000==1.13.2",
            "sqlalchemy==1.3.13",
            "timeout-decorator==0.4.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "polygonetl=polygonetl.cli:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/blockchain-etl/polygon-etl/issues",
        "Source": "https://github.com/blockchain-etl/polygon-etl",
    },
)
