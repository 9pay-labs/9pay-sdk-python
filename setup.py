from setuptools import setup, find_packages
import subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    return subprocess.check_output(
        ["git", "describe", "--tags", "--abbrev=0"]
    ).decode().strip().lstrip("v")

    
setup(
    name="ninepay-sdk",
    version=get_version(),
    author="9Pay Labs",
    author_email="support@9pay.vn",
    description="Official Python SDK for 9PAY Payment Gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/9pay-labs/9pay-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="payment gateway 9pay vietnam payment-processing",
)
