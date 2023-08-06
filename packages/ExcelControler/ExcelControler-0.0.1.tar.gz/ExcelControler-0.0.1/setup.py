from setuptools import setup, find_packages

setup(
    name="ExcelControler",
    version="0.0.1",
    keywords=["pip", "datacanvas", "excel", "holypanda"],
    description="A light weight excel to list, or list to excel package",
    long_description="A light weight excel to list, or list to excel package, base on openpyxl",
    license="Holypanda Licence",

    url="http://holypanda.me",
    author="holypanda",
    author_email="panda93222@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["openpyxl"]
)
