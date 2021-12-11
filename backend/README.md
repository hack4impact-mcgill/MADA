# Setup and Installation

Running the backend requires having some environment variables defined. To do this, create a file called `.env` at the root of the backend folder, and copy the content of `.env.dist` into your file.

Once this file is created with proper values, the app will automatically load them into the environment when run.

## Project Dependencies

First off, make sure to create a virtual environment on your machine. A virtual environment can be created with either `virtualenv` (python 2) or `venv` (python 3). For `venv`:

```
python3 -m venv env

source env/bin/activate
```

The second line activates the virtual environment, and you can type `deactivate` to exit the environment.

To install dependencies from a `requirements.txt` file, do this:

```
pip install -r /path/to/requirements.txt
```

To see all installed modules:

```
pip list
```

## Database
​Make sure you have [Docker Desktop](https://www.docker.com/get-started) on your machine.

To spin-up the database:
​
```
docker-compose up -d
```
​
To view all containers:
​
```
docker ps -a
```
​
To stop containers without removing them:
​
```
docker-compose stop
```
​
To stop containers and remove them (along with their volumes—this will drop all tables from the database!):
​
```
docker-compose down -v
```
​
The URL for the (development) database in container is `"postgresql://mada:mada@localhost:5432/postgres"`

## Flask Migrate
Please note that the migration script generated may not always be correct. When generating a migration script, please remember to go through the script in `migrations/versions/<your_migration>`.

For more information, [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

To apply latest schema changes (after pulling from `main` or a new remote branch or after generating a new migration)
```
python manage.py db upgrade
```

To generate a new migration after making changes to the schema (E.g. changing the type of a field in models.py)
```
python manage.py db migrate -m "<please put message describing change here>"
```


## Flask App Folder Structure

```
|-mu-crm-tool/
	|-backend/
		|-requirements.txt
		|-config.py # define various configurations
		|-manage.py # script for running the application
		|-app/
			|-main/
				|-__init_.py # set up Blueprint 'main' here
				|-routes.py # routes for main Blueprint here
				|-errors.py # set up error routes
			|-other_blueprint/
				|-__init_.py # set up Blueprint 'other_blueprint' here
				|-routes.py # routes for other_blueprint Blueprint here
				|-errors.py # set up error routes
			|-...
			|-__init__.py # create_app factory function goes here
			|-models.py # create model classes here
		|-tests/
	|-frontend/
		|-...
```

To run a Blueprint-based app, run `python manage.py --config development runserver`. To run all tests, run `python manage.py --config development test`.