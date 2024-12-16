# PyCon Philipines

This project serves as a boilerplate for PyCon Philippines' websites. It provides a starting point for building a website for the annual PyCon Philippines conference, as well as other PyCon-related events and initiatives.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [>= Python 3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Node/NPM](https://nodejs.org/en/)

### Installing

#### Dependency management

For python package dependency management, we use poetry. To install poetry:

##### Linux, macOS, Windows (WSL)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Spawn the virtualenv

```bash
poetry shell
```

#### Install the dependencies

```bash
poetry install
```

### Running the application

#### Run migration

```bash
python manage.py migrate
```

#### Start the server

```bash
python manage.py runserver
```

#### Start the server with livereload

```bash
python manage.py livereload
```

#### Tailwind

To work with styling and tailwind, you need to have Node/NPM installed. Install packages:

```bash
npm install
```

Then run tailwind build watcher:

```bash
npm run twbuild
```

### Coding Style

This project follows a standard coding style to ensure consistency and readability in the codebase.

#### PEP 8

We follow the guidelines outlined in [PEP 8](https://www.python.org/dev/peps/pep-0008/), the official Python style guide. This includes guidelines for naming conventions, indentation, whitespace, and more.

#### Naming Conventions

- Use `lowercase_with_underscores` for variable and function names.
- Use `CamelCase` for class names.
- Use `UPPERCASE_WITH_UNDERSCORES` for constants.

#### Indentation

- Use 4 spaces for indentation.
- Do not use tabs for indentation.

#### Whitespace

- Use a single space after commas and colons.
- Do not use spaces around parentheses, brackets, or braces.
- Use a single blank line to separate logical sections of code.

#### Line Length

- Limit lines to a maximum of 79 characters.
- When a line would exceed the limit, break it at an appropriate point and continue on the next line.

#### Comments

- Use comments to explain non-obvious code.
- Use docstrings to document functions, classes, and modules.
- Use complete sentences and proper grammar in comments and docstrings.

### Standard Commit Messages

This project follows a standard format for commit messages to ensure consistency and clarity in the commit history.

## Commit Message Format

Each commit message should consist of a single line header, followed by an optional body and footer. The header should be no more than 72 characters and should be written in the present tense. The body and footer should be separated by a blank line.

The header should follow this format:

Where `type` is one of the following:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

The `scope` is optional and should be a short description of the affected component.

The `subject` should be a brief summary of the changes.

The body should provide a more detailed description of the changes, including any relevant context or motivation.

The footer should contain any additional information, such as references to issues or pull requests.

## Built With

- [Wagtail](https://wagtail.org/) - Wagtail is the leading open-source Python CMS
- [Python](https://www.python.org/) - Python is a programming language that lets you work quickly
  and integrate systems more effectively.

### Authors

- [@zorexsalvo](https://github.com/zorexsalvo)
- [@drfb](https://github.com/drfb)
- [@pandabearcoder](https://github.com/pandabearcoder)
- [@anjlapastora](https://github.com/anjlapastora)
- [@EstopaceMA](https://github.com/EstopaceMA)

See also the list of [contributors](https://github.com/pythonph/pyconph-2024/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
