# open-oni_nebraska_theme
This is the new nebraska child theme for open-oni

## Including in the Open ONI App

Download the master branch:

```
git clone git@github.com:CDRH/open-oni_nebraska_theme.git themes/nebraska
```

In `onisite/settings_local.py`, add the theme.  Don't remove `themes.default`.

```
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'themes.nebraska',
    'themes.default',
    'core',
)

```

Also, in `onisite/urls.py`, add the Nebraska about URLs:

```
from django.conf.urls import url, include

urlpatterns = [
  url(r'^about/', include("themes.nebraska.urls")),
  url('', include("core.urls")),
]

```
