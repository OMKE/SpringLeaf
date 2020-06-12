import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='springleaf',
    version='0.1',
    scripts=['springleaf'],
    author="Omar Iriskic",
    author_email="contact@omaririskic.com",
    description="Spring Boot Code Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OMKE/springleaf",
    packages=setuptools.find_packages(),
    py_modules=["cli", "generator"],
    install_required=["jinja2", "javalang",
                      "PyInquirer", "pyyaml", "pyfiglet", "rich"],
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
