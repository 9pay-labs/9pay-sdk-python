import re
from pathlib import Path
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    changelog = Path("CHANGELOG.md").read_text()
    match = re.search(r"##\s+v?(\d+\.\d+\.\d+)", changelog)
    if match:
        return match.group(1)
    return "0.0.0"

setup(
    name="ninepay-sdk",
    version=get_version(),
    author="9Pay Labs",
    author_email="app@9pay.vn",
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
        "requests>=2.28.0",
    ],
    keywords="payment gateway 9pay vietnam payment-processing",
)
