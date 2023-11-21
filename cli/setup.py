import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read("README.md") if os.path.isfile("README.md") else ""

setup(
    name="polygon-etl",
    version="0.5.0",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="polygon",
    python_requires=">=3.7,<3.10",
    install_requires=[
        "base58==2.1.1",
        "blockchain-etl-common==1.7.1",
        "click>=8.0,<9",
        "eth-abi==2.2.0",  # web3 5.28.0 depends on eth-abi<3.0.0
        "eth-utils==1.10",  # eth-abi 2.2.0 depends on eth-utils<2.0.0
        "ethereum-dasm==0.1.5",
        "requests>=2.23",
        "six==1.16.0",  # REVIEW: Missing dependency for blockchain-etl-common
        "web3>=5.29,<6",
    ],
    extras_require={
        "streaming": [
            "google-cloud-pubsub==2.13.5",
            "google-cloud-storage==2.7.0",
            "pg8000>=1.16.6",  # SQLAlchemy 1.4.46 requires pg8000>=1.16.6
            "SQLAlchemy==1.4.46",
            "timeout-decorator==0.5.0",
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
