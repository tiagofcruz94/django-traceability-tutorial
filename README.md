# Django Traceability Tutorial

[![CI](https://github.com/tiagofcruz94/django-traceability-tutorial/actions/workflows/ci.yml/badge.svg)](https://github.com/tiagofcruz94/django-traceability-tutorial/actions)

A learning project in Python and Django that tracks beef from animals and carcasses to deboning lots.
It covers the Django admin, forms, tests and a CI workflow.

## Installation

Clone the repository:

```shell
git clone https://github.com/tiagofcruz94/django-traceability-tutorial.git
cd django-traceability-tutorial
```

Create and activate a virtual environment (Python 3.14).

On Windows (PowerShell):

```powershell
py -3.14 -m venv .venv
.venv\Scripts\activate
```

On macOS and Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Install the dependencies, create the database and an admin user, and start the server:

```shell
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/lotes/ (no login needed)
or http://127.0.0.1:8000/admin/ (log in with the user created by `createsuperuser`).

## Tests

```shell
python manage.py test
```
