# Donation counter

## How to

Dependencies are managed with poetry, it's pretty.

You can install poetry from pip by executing `pip install --user poetry`

If you want to, and I recommend this, create a virtual environment for the project.
```
python -m venv env
source env/bin/activate
```

Now install the dependencies with `poetry install`.

Start the server using the Makefile -> `make`

## Config

You have to pass the relevant tab access key to the application via the environment variable `TAB_TOKEN=_your_token_here_`

You can pass the user you want to view via the `TAB_USER` variable. Default is `teamtrees_donations` at this moment.
