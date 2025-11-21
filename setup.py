from setuptools import setup, find_packages
from setup_version import __version__

setup(
    name="1security",
    version=__version__,
    description="Open Source ASPM Orchestrator",
    author="R Jagan Raj",
    author_email="",
    url="https://github.com/jaganraj/1security",
    packages=find_packages(),
    py_modules=['cli'],
    include_package_data=True,
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.1.0",
        "jinja2>=3.1.0",
        "rich>=13.0.0",
        "checkov>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "1security=cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)

