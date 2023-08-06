# Shuup Attrim

This addons allows to create multi-value attributes for Shuup.

## Screenshots

Creation of the class `color` and assignment of a `color` attribute to a product:

<a href="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/creation-form.png">
    <img src="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/creation-form.png" width="377px">
</a>
<a href="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/assignment-form.png">
    <img src="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/assignment-form.png" width="377px">
</a>

## Online Demo

Just a bare shuup installation with the default shuup theme (`classic_gray`). The site rollbacks itself to the initial state every day.

You can login into the [admin panel](http://scatl-demo.tk/sa) using the following credentials:
- login: `demo`
- password: `demo`

The admin panel forms:
- [class creation form](http://scatl-demo.tk/sa/attrim/new/)
- [attributes assignment form](http://scatl-demo.tk/sa/products/23/) (click on the `Attrim` tab to open it)
- a [product catalog](http://scatl-demo.tk/catalog) example (made by combining `shuup-attrim` with [`shuup-scatl`](https://gitlab.com/nilit/shuup-scatl))

## Installation

Install using `pip`:
```
pip install shuup-attrim
```

Add `attrim` to your `INSTALLED_APPS` setting:
```
INSTALLED_APPS = (
    # [...]
    'attrim',
)
```

Apply the migrations:
```
python manage.py migrate
```

Collect the static files:
```
python manage.py collectstatic
```
