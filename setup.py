import setuptools
from setuptools import setup

setup(
    name="Autowire",
    packages=setuptools.find_packages(exclude=["tests"]),
    version="1.1.4",
    description="Simple dependency injection.",
    author="Choi Geonu",
    author_email="6566gun@gmail.com",
    url="https://github.com/hardtack/autowire",
    license="MIT LICENSE",
    keywords=["dependency-injection"],
    package_data={"autowire": ["py.typed"]},
)
