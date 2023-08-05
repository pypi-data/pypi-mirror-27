# `trapmk`: TrapHack Builder Script

[![PyPI](https://img.shields.io/pypi/v/trapmk.svg)](https://pypi.python.org/pypi/trapmk)

Recursive directories and build `index.html` files using [jinja2 template
files](http://jinja.pocoo.org/docs/latest/templates) named `_TRAPMK`.

To install to Python 3: `pip3 install trapmk`.

Originally created for [TrapHack](http://y2k.cafe:8080/gallery/zones/traphack).

## Example

### Prepare your site

Prepare a directory directory to look like this:

    ./some-base-template.html
    ./very-qt-shrine/_TRAPMK
    ./very-qt-shrine/pinup.pdf
    ./very-qt-shrine/qt-trap.png

In the example above, `./very-qt-shrine/index.html` will be generated
using `./very-qt-shrine/_TRAPMK` (a jinja2 template which inherits the
`./some-base-template.html` base template).

Try adding as many `_TRAPMK` files as you want! Remember: only one per
directory (they get written out to `index.html`)!

#### `./some-base-template.html`

Base templates aren't required, but they're a powerful `jinja2` feature to make
maintaining large sites significantly easier.

You can name the file whatever you want! You just need to call it from your
`_TRAPMK` files.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }}</title>
    <meta charset="UTF-8">
</head>
<body>
    {% block body %}
    {% endblock %}

    <ul>
      {% for href, text in options %}
        <li><a href="../{{ href }}/index.html">{{ text }}</a>
      {% endfor %}
    </ul>
</body>
</html>
```

#### `./very-qt-shrine/_TRAPMK`

```html
{% extends "some-base-template.html" %}
{% set title = "very qt shrine!!" %}
{%
    set options = [
        ('some-page', 'Go to other page'),
        ('/', "Go home"),
    ]
%}
{% block body %}
    {% markdown %}
    # Nice big heading1
    Holy cow! You can even use markdown content arbitrarily!

    [Pinup girl (pdf download!)](./pinup.pdf)
    {% endmarkdown %}
{% endblock %}
```

The below parses Markdown to HTML:

```
{% markdown %}
...
{% endmarkdown %}
```

### Build the site

Once your site is prepared use `trapmk .`

If we go by the example from the prep section, running `trapmk .` should
produce `./very-qt-shrine/index.html`.

A couple ways to preview:
  * `firefox ./very-qt-shrine/index.html`
  * `python3 -m http.server` and open http://localhost:8000/very-qt-shrine/
