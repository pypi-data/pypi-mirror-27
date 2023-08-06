# Shuup Scatl

This addon adds dynamic product filters (based on angular 5) to shuup.

## Features

- works through REST API
- sorting by name and price
- filtering by price with a slider
- multi-value filters (you can check out [shuup-attrim][1] addon for details)
- translation support
- works out of the box with the default shuup theme
- human-readable url parameters, example: `scatl-demo.tk/catalog;filter.attrim.resolution=1920x1080;filter.price=674~3572;sort=name;page=1`

## Online Demo

Just a bare shuup installation with the default shuup theme (`classic_gray`). The site rollbacks itself to the initial state every day.

You can log in to the [admin panel](http://scatl-demo.tk/sa) using the following credentials:
- login: `demo`
- password: `demo`

Pages:
- [product catalog](http://scatl-demo.tk/catalog)
- [multi-value filters management](http://scatl-demo.tk/sa/attrim/)

## Screenshots
<a href="https://gitlab.com/nilit/shuup-scatl/raw/master/docs/1.png">
    <img src="https://gitlab.com/nilit/shuup-scatl/raw/master/docs/1.png" width="377px">
</a>
<a href="https://gitlab.com/nilit/shuup-scatl/raw/master/docs/2.png">
    <img src="https://gitlab.com/nilit/shuup-scatl/raw/master/docs/2.png" width="377px">
</a>

## Installation

Requires a PostgreSQL database.

Install using `pip`:
```
pip install shuup-scatl
```

Add `attrim` (a dependency) and `scatl` to your `INSTALLED_APPS` setting:
```python
INSTALLED_APPS = [
    # [...]
    'attrim',
    'scatl',
]
```

Apply the migrations:
```
python manage.py migrate
```

Collect the static files:
```
python manage.py collectstatic
```


[1]: https://gitlab.com/nilit/shuup-attrim
