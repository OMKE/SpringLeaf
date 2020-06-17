import json

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


__version__ = None
with open("springleaf/version.py") as f:
    exec(f.read())


setuptools.setup(
    name='springleaf',
    version=__version__,
    author="Omar Iriskic",
    author_email="contact@omaririskic.com",
    maintainer="Omar Iriskic",
    maintainer_email="contact@omarirsikic.com",
    scripts=["springleaf/springleaf"],
    description="Spring Boot Code Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OMKE/springleaf",
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "examples"]),
    include_package_data=True,
    package_data={
        '': ["*.json"]
    },
    py_modules=["cli", "generator", "file_handler",
                "java_parser", "prompt_builder", "exceptions"],
    install_requires=["jinja2", "javalang",
                      "questionary", "pyyaml", "pyfiglet", "rich", "prompt_toolkit==3.0.2", "jinja2"],
    keywords="spring boot cli code generator",
    project_urls={
        "Bug Reports": "https://github.com/OMKE/SpringLeaf/issues",
        "Source": "https://github.com/OMKE/SpringLeaf",
    },
    download_url="https://github.com/OMKE/SpringLeaf/archive/{}.tar.gz".format(
        __version__),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
