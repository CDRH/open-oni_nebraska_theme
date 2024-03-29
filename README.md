# open-oni_nebraska_theme
This is the new nebraska child theme for open-oni

## Including in the Open ONI App

Clone the Open ONI repository's latest v1.0.x tag and add the Nebraska theme to the `themes` directory.
If you are upgrading from v0.1.x, you will need to remove
`sass_processor` from `onisite/settings_local.py`.

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

## Load Plattsmouth Papers

Until such time as the LoC updates their Marc records from OCLC, you need to include this line in your `settings_local.py` file before you can load any of the Plattsmouth batches.  All other batches will not load while this line is in your settings, so remember to comment it or remove it after loading Plattsmouth:

```
MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/CDRH/open-oni_nebraska_theme/master/marc/%s/marc.xml"
```

## Compile Assets

Compile `main.scss` to `main.css` with [Sass command line
tool](https://sass-lang.com/install):

```bash
sass static/css/main.scss static/css/main.css
```

[See nebraska oni docs](docs/openoni.md#compile-static-assets)

## Load Batch Quick Reference

Upload your batch files to `/var/local/newspapers/(batch_name)`. Then run:

```bash
sudo chmod -R g+rwX /var/local/newspapers/(batch_name)
sudo chmod -R o+rX /var/local/newspapers/(batch_name)
```

Then run the following commands from the base of the Nebraska open-oni install as a regular user, NOT as root.

```bash
source ENV/bin/activate

./manage.py load_batch /var/local/newspapers/(batch_name)/

# For batches to be visible in /batches page, must be released
# Add --reset flag to clear release dates and recalculate them
# Release date and time come from:
# 1. bag-info.txt, if found in the batch source
# 2. Tab-delimited CSV file if provided in format: batch_name \t batch_date
# 3. http://chroniclingamerica.loc.gov/batches.xml
# 4. Current server datetime
./manage.py release
```

If you want to chain together multiple batches, or you want to prevent scripts from exiting if the terminal shell is closed / session disconnects, run `nohup` with a command or script.

```bash
nohup (command) >> nohup.out
```
