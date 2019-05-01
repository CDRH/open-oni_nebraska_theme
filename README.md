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

You will need to clone and configure these as well or else the theme's navigation will not work as intended.  Follow instructions in those repositories for customizing the contents of the map and the featured content using the files in this theme's `conf/plugins` directory.

```
git clone git@github.com:open-oni/plugin_calendar.git onisite/plugins/calendar
git clone git@github.com:open-oni/plugin_featured_content.git onisite/plugins/featured_content
git clone git@github.com:open-oni/plugin_map.git onisite/plugins/map
```

Copy in Nebraska configuration for the calendar plugin (these may differ if the plugin has been changed and our theme has not yet been updated):

```
# calendar
cp themes/nebraska/conf/plugins/calendar/config.py onisite/plugins/calendar/config.py
```

### Django Settings
[Configure app settings](/docs/openoni.md#local-settings)
to use the theme and plugins
as well as display the appropriate site title and project name

[Set `urls.py`](/docs/openoni.md#urls) to use the theme and plugins

## Plugin Customization

We will be adding a one-stop command that will set up the customizations for each of the plugins, but in the meantime just to get a basic version of the plugin, follow the instructions in each's readme.

### Calendar

[Plugin Calendar Repo](https://github.com/open-oni/plugin_calendar)

This calendar replaces the less accessible original calendar. You will need to copy the Nebraska theme's config file.

### Featured Pages

[Featured Pages Repo](https://github.com/open-oni/plugin_featured_content)

You do not need to copy the `featured_example.html`, as the `featured.html` file is already at `themes/nebraska/templates/featured.html`.

TODO
- select specific featured pages from our currently loaded options, then add that config file and copying process to this repository

UNTIL THEN
- Copy config demo file to `onisite/plugins/featured_content/config.py`

### Map

[Plugin Map Repo](https://github.com/open-oni/plugin_map)

The JS file containing the map locations does not need to be moved into the plugin. It lives in `themes/nebraska/static/js/cities_list.js`.  You will need to update it when any new titles are added.

TODO
- consider adding lat / lng to titles in the database, otherwise update the existing list `themes/nebraska/static/js/cities_list.js` as needed

## Load Plattsmouth Papers

Until such time as the LoC updates their Marc records from OCLC, you need to include this line in your `settings_local.py` file before you can load any of the Plattsmouth batches.  All other batches will not load while this line is in your settings, so remember to comment it or remove it after loading Plattsmouth:

```
MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/CDRH/open-oni_nebraska_theme/master/marc/%s/marc.xml"
```

## Compile Assets

[See nebraska oni docs](docs/openoni.md#compile-static-assets)
