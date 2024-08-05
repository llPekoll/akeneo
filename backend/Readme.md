# Secret Santa Backend

This is the backend part of the Secret Santa application. It provides APIs to manage participants, blacklists, and draw results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)

## Installation

### Prerequisites

- Python 3.8+
- Django 4.2+
- Django REST framework

### Setup

1.  Clone the repository:

        ```bash
        git clone https://github.com/yourusername/secret-santa.git
        cd secret-santa/backend
        ```

2.  Create a virtual environment and activate it:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  Install the required packages:

        ```bash
        pip install -r requirements.txt
        ```

4.  Apply migrations:

        ```bash
        python manage.py migrate
        ```

5.  Create a superuser:

        ```bash
        python manage.py createsuperuser
        ```

6.  Run the development server:

        ```bash
        python manage.py runserver
        ```

## Usage

### Accessing the Admin Panel

You can access the Django admin panel at `http://127.0.0.1:8000/admin` and log in with the superuser credentials you created.
But this par hasn't been setuped as it was not requested in the test

### API Endpoints

http://127.0.0.1:8000/ for api access
A swagger also could haven't been added to the project to make it easier to access the API

But here is the backend provides the following API endpoints:

- **Participants**

  - `GET /api/participants/` - List all participants
  - `POST /api/participants/` - Create a new participant

- **Blacklists**

  - `GET /api/blacklists/` - List all blacklists
  - `POST /api/blacklists/` - Create a new blacklist

- **Draws**
  - `POST /api/draws/` - Create a new draw

### Example Requests

#### List Participants

```bash
curl -X GET http://127.0.0.1:8000/api/participants/
```

## Running Tests

To run the tests, use the following command:

```python
python manage.py test
```

This will execute the test suite and ensure that all functionalities are working as expected.
Test has been limited to hard code inputs. with more time we could have used a library such as `Faker`
