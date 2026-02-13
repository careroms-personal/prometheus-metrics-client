"""
Setup file for prometheus-metrics-client
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name="prometheus-metrics-client",
  version="0.1.0",
  author="Your Name",
  author_email="your.email@example.com",
  description="A Python client for querying Prometheus/Mimir metrics with multi-platform support",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/yourusername/prometheus-metrics-client",
  packages=find_packages(),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: System :: Monitoring",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
  ],
  python_requires=">=3.9",
  install_requires=[
      "requests>=2.31.0",
  ],
)