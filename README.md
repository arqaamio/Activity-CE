Activity
====

We are developing a tool for humanitarians to manage project activities and indicator results across their programs, including approval workflows and reporting and visualizations. Our goal is to help organizations answer common questions such as:
* who are funding your projects?
* who you work with?
* where you work?
* how do my outputs align with my overall project goal?

<!-- ## Configuration
Copy the activity/settings/local-sample.py to local.py and modify for your environment.

## To deploy changes in activity servers
Once all your changes have been committed to the repo, and before pushing them, run:
`. travis.sh` -->

<!-- ## To deploy locally via Docker
Run the following commands from the root of this repository:

NB: Ensure you have docker installed on your machine
  - `docker-compose build .`
  # run  migrations
  - `docker-compose run web python /code/manage.py migrate --noinput`
  # create superuser
  - `docker-compose run web python /code/manage.py createsuperuser`
  # start the app
  - `docker-compose up -d --build`
  # open on browser
  - `http://127.0.0.1:8000/` -->

# Local Setup

Note: you should use python 3 for this project, meaning you may need to use `python3` or `pip3` in the following instructions (you can use the package manager on your OS, brew for mac, to install python 3).

Open up your terminal and follow the instructions listed below.

See [these instructions for installing known dependencies](#install-non-python-dependencies).

## Clone the github repository

Navigate to the folder you want the repository to be stored in.

Run the following command:
```bash
$ git clone --branch dev https://github.com/hikaya-io/Activity.git
```

Once cloned, navigate to the cloned repository with:
```bash
$ cd Activity
```
or similar.

## Install virtualenv

```bash
$ pip install virtualenv
```

## Create virtualenv

```bash
$ virtualenv --no-site-packages <myvirtualenvironmentname>
```
* use no site packages to prevent virtualenv from seeing your global packages
* . <myvirtualenvironmentname>/bin/activate allows us to just use pip from the command-line by adding to the path rather then full path.

## Activate virtualenv

```bash
$ source <myvirtualenvironmentname>/bin/activate
```

## Install requirements

```bash
$ pip install -r requirements.txt
```

## Create local copy of config file

Copy the example config:
```bash
$ cp activity/settings/local-sample.py activity/settings/local.py
```

## Modify the config file
Edit database settings activity/settings/local.py as shown below.

We will change the `ENGINE` parameter to the default value for postgres (although you can also user MySQL or Sqllite3 which is out-of-the-box supported by Django). We also need to add a default database name in the `NAME` option.

Since postgres is the preferred database for this project, we have provided extra instructions to help you set it up. These can be viewed [here](#postgresql-help).

```yaml
47 DATABASES:
48  'default': {
49    #'ENGINE': 'django.db.backends.postgresql', # Alternatives: 'postgresql', 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
50    'ENGINE': "django.db.backends.postgresql"
51    'NAME': os.environ.get('ACTIVITY_CE_DB_NAME', 'mydatabasename'), # replace mydatabasename here with the name of your database
# The following can be left unchanged for local use:
52    'USER': os.environ.get('ACTIVITY_CE_DB_USER', ''),
53    'PASSWORD': os.environ.get('ACTIVITY_CE_DB_PASSWORD', ''),
54    'HOST': os.environ.get('ACTIVITY_CE_DB_HOST', ''),
55    'PORT': os.environ.get('ACTIVITY_CE_DB_PORT', ''),
```

## Set up DB

```bash
$ python manage.py migrate
```

## Create super user (first run only)

```bash
$ python manage.py createsuperuser
```

# Run the app locally

If your using more then one settings file change manage.py to point to local or dev file first.
```bash
$ python manage.py runserver
```

<!-- ## GOOGLE API
```bash
$ sudo pip install --upgrade google-api-python-client
``` -->

This will run the server on http://127.0.0.1:8000. You can configure the host and port as needed.

# Extra information

## Install non-python dependencies

1. **GDAL**

On mac:
```bash
$ brew install gdal
```

2. **pango**

On mac:
```bash
$ brew install pango
```

## Postgresql help

### Install

On mac:
```bash
$ brew update
$ brew install postgresql
$ initdb /usr/local/var/postgres
$ pg_ctl -D /usr/local/var/postgres start
$ createdb <mydatabasename>
```

### Manage

```bash
pg_ctl -D /usr/local/var/postgres start # to start
pg_ctl -D /usr/local/var/postgres stop # to stop
```

## MySQL help

### Django migrate access denied

If you get access denied, it means you need to modify the config file and write your Mysql username and password in the file

### Path issue

To fix any issues related to your path that may come up during the django set up, run:
```bash
$ export PATH=$PATH:/usr/local/mysql/bin
```
or specify the path you have to your installed mysql_config file in the bin folder of mysql

If you want this environment variable to be automatically set, please include it in your bash_profile or bashrc file.

### Django settings file
Replace user and password by your Mysql username and password

### Set up Django's MySQL backing store
```sql
CREATE DATABASE 'activity';
CREATE USER 'root';
GRANT ALL ON activity.* TO 'root'@'localhost' IDENTIFIED BY 'root';
```
*NB:* When you use these SQL queries, beware of not writing the quotes.
