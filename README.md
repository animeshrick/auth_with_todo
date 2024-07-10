Create your virtual-environment for `AUTH_WITH_TODO` outside of the project root directory.

```bash
  python -m venv devenv
  .\devenv\Scripts\activate
```

Now install all the dependencies in auth-env.

```bash
  pip install -r .\dependencies\dev-requirements.txt
```

To run

```bash
  python app.py
```