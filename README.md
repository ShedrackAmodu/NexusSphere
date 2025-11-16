# NexusSphere — Phase 1

Minimal Django project skeleton for Phase 1.

Quick start

1. Create and activate a virtualenv (recommended).
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Apply migrations and run the server:

```powershell
python manage.py migrate
python manage.py runserver
```

4. Open http://127.0.0.1:8000/ to see the homepage.

Running tests

```powershell
python manage.py test
```

Phase 3 — Authentication and CI
--------------------------------

This project now protects create/update/delete operations on `Item` behind authentication.

- To create a staff/superuser for local development run:

```powershell
python manage.py createsuperuser
```

- Visit http://127.0.0.1:8000/accounts/login/ to sign in. The app shows Login/Logout links in the header.

Continuous Integration
----------------------

A GitHub Actions workflow was added at `.github/workflows/ci.yml`. On push and pull requests to `main` it will:

1. Install dependencies from `requirements.txt`.
2. Run `python manage.py migrate`.
3. Run the test suite with `python manage.py test`.

If you want me to extend the workflow (matrix for multiple Python versions, caching pip, or add linting/coverage), tell me and I will add it.

