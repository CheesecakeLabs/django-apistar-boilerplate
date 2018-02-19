# {{ Project name here }}

## Installation

1. Clone this repo:
  - `git clone https://github.com/CheesecakeLabs/django-apistar-boilerplate.git`

1. Create a virtualenv and activate it:
  - Using `virtualenv`:
    - `virtualenv venv`
    - `. venv/bin/activate`
  - Using `pyenv`:
    - `pyenv virtualenv 3.6.4 <project-name>`
    - `pyenv activate <project-name>`
1. Install dependencies:
  - `pip install -r requirements`


## Running the local server

The settings file contains default values for environment variables, but if needed, copy the
`local.env.example` file to `local.env` and add the correct variables values. After that:

1. `cd src`
1. `apistar run`


## Running tests

1. `pyest`

Note: Tests are configured to use SQLite database. You can change this configuration on
`pytest.ini` file.
