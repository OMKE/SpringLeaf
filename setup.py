import json

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("springleaf/common/version.json", "r") as file:
    version = json.load(file)["version"]


setuptools.setup(
    name='springleaf',
    version=version,
    author="Omar Iriskic",
    scripts=["springleaf/springleaf"],
    author_email="contact@omaririskic.com",
    description="Spring Boot Code Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OMKE/springleaf",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        '': ["*.json"]
    },
    py_modules=["cli", "generator"],
    install_required=["jinja2", "javalang",
                      "PyInquirer", "pyyaml", "pyfiglet", "rich"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
