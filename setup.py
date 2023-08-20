"""Python setup.py for wqu_piotroski package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("wqu_piotroski", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="wqu_piotroski",
    version=read("wqu_piotroski", "VERSION"),
    description="Awesome wqu_piotroski created by jsl2",
    url="https://github.com/jsl2/wqu-piotroski/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="jsl2",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["wqu_piotroski = wqu_piotroski.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
