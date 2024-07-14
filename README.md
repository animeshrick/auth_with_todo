Create your virtual-environment for `AUTH_WITH_TODO` outside of the project root directory.

```bash
  python -m venv devenv
  .\devenv\Scripts\activate
```

Now install all the dependencies in auth-env.

```bash
  pip install -r requirements.txt
```

To run

```bash
  python main.py
```


To update requirements.txt
```bash
pip freeze > requirements.txt
```

Configure Redis connection
```
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(f'redis://{redis_host}:{redis_port}')
```

SQLITE
```
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
```

postgresql
```
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{password}@localhost/{database}'
```
