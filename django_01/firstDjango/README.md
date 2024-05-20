# Django mostly used commands

## Overview

This repository contains a Django project, a high-level Python web framework that encourages rapid development and clean, pragmatic design. Django is designed to help developers take applications from concept to completion as quickly as possible.

## Prerequisites

Ensure you have the following installed:

- Python (3.6, 3.7, 3.8, 3.9, or 3.10)
- pip (Python package installer)

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/azaadmottan/Django.git
    cd django_01
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations to set up your database**:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser for accessing the admin interface**:

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

7. **Access the application**:

    Open your web browser and go to `http://127.0.0.1:8000/`

## Commonly Used Commands

### Project Management

- **Start a new Django project**:

    ```sh
    django-admin startproject projectname
    ```

- **Start a new app within your project**:

    ```sh
    python manage.py startapp appname
    ```

### Database Management

- **Make migrations** (generate SQL for your model changes):

    ```sh
    python manage.py makemigrations
    ```

- **Apply migrations** (apply the generated SQL to the database):

    ```sh
    python manage.py migrate
    ```

- **Check for migration issues**:

    ```sh
    python manage.py makemigrations --check
    ```

### User Management

- **Create a superuser** (for accessing the admin interface):

    ```sh
    python manage.py createsuperuser
    ```

### Running the Server

- **Run the development server**:

    ```sh
    python manage.py runserver
    ```

- **Run the development server on a specific IP and port**:

    ```sh
    python manage.py runserver 0.0.0.0:8000
    ```

### Shell and Data Management

- **Open the Django shell** (interactive Python shell with Django context):

    ```sh
    python manage.py shell
    ```

- **Load data from a fixture**:

    ```sh
    python manage.py loaddata fixture_name
    ```

- **Dump data to a fixture**:

    ```sh
    python manage.py dumpdata app_label.ModelName --output=filename.json
    ```

### Testing

- **Run tests**:

    ```sh
    python manage.py test
    ```

### Static Files Management

- **Collect static files** (for production deployment):

    ```sh
    python manage.py collectstatic
    ```

### Miscellaneous

- **Check for potential problems in the project**:

    ```sh
    python manage.py check
    ```

- **View SQL for a migration**:

    ```sh
    python manage.py sqlmigrate appname migration_number
    ```

---

Happy coding!
