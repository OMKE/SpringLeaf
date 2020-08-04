# Spring Leaf

[![version](https://img.shields.io/pypi/v/springleaf.svg)](https://pypi.org/project/springleaf/)
[![license](https://img.shields.io/pypi/l/springleaf.svg)](https://pypi.org/project/springleaf/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/springleaf.svg)](https://pypi.python.org/pypi/springleaf)

🍃 Easy to use Spring Boot CLI 🍃 <br>

SpringLeaf CLI creates, manages, builds and test your SpringBoot Applications

## Quickstart

To install `springleaf`, use pip: <br>
`$ pip install springleaf`

## Description

SpringLeaf is All In One CLI for your Spring Boot Applications <br>
Some of the features are:

<ul>
    <li>Generating DTOs, Repositories, Services, Request and Response classes out of Entity model</li>
    <li>Initializing new Spring Boot project with SpringInitializr - Maven, Gradle (not yet supported)</li>
</ul>

## Usage

### Code generation

![spring-code-generation-example-gif](docs/images/generate.gif)

### SpringInitializr

![spring-initializr-example-gif](docs/images/spring_initializr.gif)

- @TODO (custom folder structures)

## Changelog

<details><summary>Version: 0.4.1</summary>
    Bug fixes in template files: <br>
        <ul>
            <li>Fixed import bugs in templates.</li>
        </ul>

</details>
<details><summary>Version: 0.4</summary>
    Main functionality and bug fixes: <br>
        <ul>
            <li>Main functionality of generator works.</li>
            <li>Generate files with standard or basic folder structure.</li>
            <li>Autowiring when all files are selected for generation.</li>
            <li>Bugfixes*</li>
        </ul>

</details>
<details><summary>Version: 0.3</summary>
    Updates and bugfixes: <br>
        <ul>
            <li>Handled KeyboardInterrupt Exceptions</li>
            <li>Added more checks for checkboxes</li>
            <li>Added controller-type key so user can choose between @Controller and @RestController</li>
            <li>Bugfixes</li>
        </ul>

</details>
<details><summary>Version: 0.2</summary>
    Feature release: <br>
        <ul>
            <li>Added SpringInitializr</li>
            <li>Maven is only supported for now, Gradle support will come in future relases</li>
        </ul>

</details>
<details><summary>Version: 0.1.2</summary>
    Windows: <br>
        <ul>
        <li>Moved from PyInquirer(not in development) to <a href="https://github.com/tmbo/questionary/">questionary</a> , error was still appearing in CommandPrompt</li>
        <li>Founded out that everything works in Cmder when started in bash </li>
        <li>Should be tested more on Windows</li>
        <li>changed prompt_toolkit version to 3.0.2</li>
        </ul>
</details>
<details><summary>Version: 0.1.1</summary>
    Windows: <br>
        <ul>
            <li>Error in CommandPrompt with prompt_toolkit (Exception: NoConsoleScreenBufferError), tried with version <=2.0, <br>
                error was still appearing</li>
        </ul>

</details>

## Packages

| Package     | Link                                                                    | Description                                                                      |
| :---------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| questionary | <a href="https://github.com/tmbo/questionary">@tmbo/questionary</a>     | An easy to use python library to build pretty command line user prompts          |
| jinja2      | <a href="https://github.com/noirbizarre/jinja2">@noirbizarre/jinja2</a> | Jinja2 is a template engine written in pure Python.                              |
| javalang    | <a href="https://github.com/c2nes/javalang">@c2nes/javalang</a>         | javalang is a pure Python library for working with Java source code              |
| rich        | <a href="https://github.com/willmcgugan/rich">@willmcgugan/rich</a>     | Rich is a Python library for rich text and beautiful formatting in the terminal. |
| pyfiglet    | <a href="https://github.com/pwaller/pyfiglet">@pwaller/pyfiglet</a>     | An implementation of figlet written in Python                                    |
| pyyaml      | <a href="https://github.com/yaml/pyyaml">@yaml/pyyaml</a>               | YAML parser and emitter for Python                                               |

## License

Licensed under the MIT License. Copyright 2020 Omar Iriskic
