# open-oni_nebraska_theme
This is the new nebraska child theme for open-oni

## Including in the Open ONI App

Clone the Open ONI repository's v0.10.0 tag and add the Nebraska theme to the `themes` directory

```
git clone git@github.com:open-oni/open-oni.git open-oni
cd open-oni
git checkout tags/v0.10.0
git clone git@github.com:CDRH/open-oni_nebraska_theme.git themes/nebraska
```

The Nebraska theme depends upon several plugins:

- [Accessible Calendar](https://github.com/open-oni/plugin_calendar)
- [Featured Content](https://github.com/open-oni/plugin_featured_content)
- [Map](https://github.com/open-oni/plugin_map)

You will need to clone and configure these as well or else the theme's navigation will not work as intended.  Follow instructions in those repositories for customizing the contents of the map and the featured content.

```
git clone git@github.com:open-oni/plugin_calendar.git onisite/plugins/calendar
git clone git@github.com:open-oni/plugin_featured_content.git onisite/plugins/featured_content
git clone git@github.com:open-oni/plugin_map.git onisite/plugins/map
```

In `onisite/settings_local.py`, add the theme and plugins.  Don't remove `themes.default`.  Also configure the application's title settings.

```
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'onisite.plugins.calendar',
    'onisite.plugins.featured_content',
    'onisite.plugins.map',

    'themes.nebraska',
    'themes.default',
    'core',
)

SITE_TITLE = "Nebraska Newspapers"
PROJECT_NAME = "Nebraska Newspapers"
```

Also, in `onisite/urls.py`, add the Nebraska about URLs:

```
from django.conf.urls import url, include

urlpatterns = [
  url('', include("onisite.plugins.calendar.urls")),
  url('', include("onisite.plugins.featured_content.urls")),
  url(r'^map', include("onisite.plugins.map.urls")),

  # you can customize where the featured_content is viewed with this url
  # url(r'^featured_content', include("onisite.plugins.featured_content.urls")),

  url('', include("themes.nebraska.urls")),
  url('', include("core.urls")),
]
```

## Plugin Customization

We will be adding a one-stop command that will set up the customizations for each of the plugins, but in the meantime just to get a basic version of the plugin, follow the instructions in each's readme.

### Calendar

[Plugin Calendar Repo](https://github.com/open-oni/plugin_calendar)

This calendar replaces the less accessible original calendar. You do not need to customize this plugin.

### Featured Pages

[Featured Pages Repo](https://github.com/open-oni/plugin_featured_content)

TODO
- setup with specific page rotation (this will only work if those batches are loaded), set to random (existing) pages by default

UNTIL THEN
- Copy config demo file to `onisite/plugins/featured_content/config.py`

### Map

[Plugin Map Repo](https://github.com/open-oni/plugin_map)

TODO
- consider adding lat / lng to titles in the database, otherwise update the existing list `static/js/cities_list.js` as needed

## Load Plattsmouth Papers

Until such time as the LoC updates their Marc records from OCLC, you need to include this line in your `settings_local.py` file before you can load any of the Plattsmouth batches.  All other batches will not load while this line is in your settings, so remember to comment it or remove it after loading Plattsmouth:

```
MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/CDRH/open-oni_nebraska_theme/master/marc/%s/marc.xml"
```
