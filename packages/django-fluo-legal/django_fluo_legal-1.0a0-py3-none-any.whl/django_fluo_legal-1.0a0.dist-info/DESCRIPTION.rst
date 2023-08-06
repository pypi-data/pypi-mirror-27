# django-fluo-legal #
A Django application to handle european/italian cookie law and versioned T&C.

## install ##
Just include `legal.apps.LegalConfig` into your `INSTALLED_APPS`
```
#!python

INSTALLED_APPS += [ "legal.apps.LegalConfig" ]
```


## templatetag ##
Show an overlay box to inform about privacy/cookies.

Load the templatetag in your base template
```
#!html
{% load legal_tags %}

  ...
  {% cookielaw %}
  </body>
</html>
```

You can customize the box overriding `templates/legal/cookielaw.css`
and/or `templates/legal/cookielaw.html` or using the templatetag
parameters:

* `banner`: [default=`legal/cookielaw.html`]
* `name`: [default=`legal_cookielaw_accepted`]
* `id`: [default=`CookieLawBanner`]
* `js`: [default=`legal/cookielaw.js`]
* `css`: [default=`legal/cookielaw.css`]


