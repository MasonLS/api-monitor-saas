from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-monitor-saas",
    version="0.1.0",
    author="Mason Seale",
    author_email="mason.seale@ae.studio",
    description="A simple, effective API monitoring service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MasonLS/api-monitor-saas",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "flask>=3.0.0",
        "schedule>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "api-monitor=src.monitor:main",
            "api-dashboard=src.dashboard:main",
        ],
    },
)
