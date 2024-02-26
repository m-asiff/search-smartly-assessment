## Pre-requisites

[Download and install Python 3.10.1 or a suitable version](https://www.python.org/downloads/release/python-31010/)


### Activate the virtual environment

For Unix-based systems:
```shell
python -m venv .venv
source .venv/bin/activate
```

For Windows:
```shell
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```shell
pip install -r requirements.txt
```

### Run database migrations

```shell
python manage.py migrate
```
   
### Import data from file
```shell
python manage.py import_data path_to_file
```
   
### Create a superuser to access admin site
```shell   
python manage.py createsuperuser
```

### Run the development server
```shell
python manage.py runserver 
```

### Run tests
```shell
pytest
```

### Run Linting Check
```shell
flake8
```

## Implementation Details
Below is an overview of the key components and their implementation details:

### Application Structure
**Models:** Defined in app/models.py, models represent the application's data structure. This project includes models for Category and Poi (Points of Interest), with fields corresponding to their properties in the database.

**Views:** Located in app/views.py, views handle the request/response logic. The poi_list_view function demonstrates querying the database based on search parameters and paginating the results.

**Templates:** HTML templates are stored in app/templates/. They render the data passed from views and utilize Bootstrap for styling. The searchfilter_template.html is used to display search forms and paginated results.

**URLs:** URL patterns are defined in app/urls.py. They map URLs to their corresponding views in the application.

**Admin:** Django's admin interface is used for easy management of the database records. Models are registered in app/admin.py to make them accessible via the admin panel.

**Management Commands:** Custom commands, such as import_data, are defined in app/management/commands/. These allow for operations like importing data from files into the application's database.

### Key Features
**Search and Filter:** Users can search for Points of Interest by internal ID, external ID, or category. The application filters the database records based on the provided search criteria.

**Pagination:** The application implements pagination to limit the number of results displayed at once, improving the usability for datasets with many entries.

**Data Import:** A custom Django management command import_data is implemented to facilitate the importation of data from specified files into the application's database, supporting various file formats.

### Data Management
**Database Setup:** Initial setup involves running migrations to create database tables based on the application's models.

**Superuser Creation:** For administrative tasks, a superuser account can be created, granting access to Django's built-in admin interface.

**Data Importation:** The import_data management command allows for the bulk importation of data, streamlining the process of populating the application's database with initial data.

### Development and Testing
***Development Server:*** Django includes a lightweight web server for development and testing purposes, which can be started with the runserver command.

***Testing:*** The framework's testing tools are used to write and run tests, ensuring the application's functionality works as expected.
