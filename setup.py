import json

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='springleaf',
    version="0.1.2",
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
    py_modules=["cli", "generator", "file_handler",
                "java_parser", "prompt_builder", "exceptions"],
    install_requires=["jinja2", "javalang",
                      "questionary", "pyyaml", "pyfiglet", "rich", "prompt_toolkit==3.0.2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
