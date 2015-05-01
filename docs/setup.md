# Setting up a Fresh Install of Kitherder

# Requirements
Kitherder requires the following:
* Python 2.7.5
* Django 1.4.3
* argparse 1.2.1
* distribute 0.6.24
* django-browserid 0.9
* fancy-tag 0.2.0
* requests 2.2.1
* six 1.5.2
* wsgiref 0.1.2
* A Mozillian API key

# To install
1. Download all of Kitherder and place in an easily accessible directory
2. Look for the settings.py file under the kitherder directory and open with a text editor (For the following edits, you may see /kitherder/kitherder/settings-renee-home.py as an example)
	a. Go to line 151 and edit the URL to reflect the proper URL
	b. Go to line 15 to edit the appropriate directory where the SQL database will reside
	c. Go to line 82 and replace if necessary with the absolute path of where static folder is. (ending with ../kitherder/kitherder/static/)
	d. Replace line 117 with the absolute path of where kitherder resides (ending with ../kitherder/kitherder)
	e. Go to the end of the file and look for the variables MOZILLIAN_URL and MOZILLIAN_APP_KEY. Place the information for the Mozillian instance you are connecting to here.
3. In the folder kitherder/kitherder/matchmaker/fixtures, there is an initial_data.json file. If you require initial values beyond what is there, you may edit this file. However, what is currently in there should be sufficient to start.
4. In command line, navigate to the kitherder folder and run the following command
<code>python manage.py syncdb</code>
	a. As part of the process, it should ask you to create a new user and password. You will require this username and password to setup the rest of Ktiherder.
5. To run kitherder, run the following command
<code>python manage.py runserver</code>

Kitherder should now be up and running.

# Setting up Kitherder
1. Using a browser, navigate to Kitherder
2. Login in and register as a mentor. (You should be a vouched Mozillian so should not have any trouble doing so.)
3. Navigate to the Django admin interface
4. Set up divisions as required.
5. Add in corresponding coordinators to the divisions as required.

Kitherder should now be ready for use.
