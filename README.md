# How to run the application

First clone the repository

```bash
git clone https://github.com/asifrahaman13/costarica-levato
```

Create the virtual environement.

```bash
virtualenv .venv
source .venv/bin/activate
```

Next you can install the required packages and libraries.

```bash
pip install -r requirements.txt
```

Create a .env file from the .env.exmaple

```bash
cp .env.example .evn
```

Next enter the credential for the postgres database.

Now you can run the Jupyter notebooks using the virtual env kernel.
