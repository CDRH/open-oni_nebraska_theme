# Open ONI Nebraska Theme
This is the Nebraska child theme for Open ONI

## Including in the Open ONI App

Clone Open ONI repository and add Nebraska theme to the `themes` directory

```bash
git clone git@github.com:open-oni/open-oni.git
cd open-oni
git clone git@github.com:CDRH/open-oni_nebraska_theme.git themes/nebraska
```

The Nebraska theme depends upon several plugins:

- [Accessible Calendar](https://github.com/open-oni/plugin_calendar)
- [Featured Content](https://github.com/open-oni/plugin_featured_content)
- [Map](https://github.com/open-oni/plugin_map)

You will need to clone and configure these as well or else the theme's navigation will not work as intended.  Follow instructions in those repositories for customizing the contents of the map and the featured content using the files in this theme's `conf/plugins` directory.

```bash
git clone git@github.com:open-oni/plugin_calendar.git onisite/plugins/calendar
git clone git@github.com:open-oni/plugin_featured_content.git onisite/plugins/featured_content
git clone git@github.com:open-oni/plugin_map.git onisite/plugins/map
```

Copy in Nebraska configuration for the calendar plugin (these may differ if the plugin has been changed and our theme has not yet been updated):

```bash
cp themes/nebraska/conf/plugins/calendar/config.py onisite/plugins/calendar/config.py
```

The calendar and map plugins require changes to their files to have page titles
and headers match the nav link texts we changed. Copy these files from
`conf/plugins/calendar/` and `conf/plugins/map/` to the corresponding
directories in `openoni/onisite/plugins/`.

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

Copy plugin's example config file to `onisite/plugins/featured_content/config.py`
and change to use "This day in history" function. Review whether min and max
years are accurate by sorting on the `/newspapers` page.

```python
# Set to True to enable the 'This day in history' function
THISDAY = True

# Set to earliest year to search with THISDAY
MINYEAR = 1854

# Set to latest year to search  with THISDAY
MAXYEAR = 2001
```

### Map

[Plugin Map Repo](https://github.com/open-oni/plugin_map)

The JS file containing the map locations does not need to be moved into the plugin. It lives in `themes/nebraska/static/js/cities_list.js`.  You will need to update it when any new titles are added.

TODO
- consider adding lat / lng to titles in the database, otherwise update the existing list `themes/nebraska/static/js/cities_list.js` as needed

## Compile Assets

Compile `main.scss` to `main.css` with [Sass command line
tool](https://sass-lang.com/install):

```bash
sass static/css/main.scss static/css/main.css
```

For production, one must run additional commands to
[Compile Static Assets](docs/openoni.md#compile-static-assets)

## Batch Management

For loading newspaper data into the Open ONI see
[Batch Management documentation](docs/batch-management.md)
