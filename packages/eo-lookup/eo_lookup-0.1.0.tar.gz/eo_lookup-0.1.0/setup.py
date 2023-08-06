import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
    README = f.read()

setup(
    name="eo_lookup",
    version="0.1.0",
    description="Esperanto dictionary lookup tool",
    long_description=README,
    url="https://github.com/open-esperanto/eo-lookup",
    author="Open Esperanto",
    author_email="admin@libraro.net",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    keywords="esperanto",
    py_modules=["eo_lookup"])
