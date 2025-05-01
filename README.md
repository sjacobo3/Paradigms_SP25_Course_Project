# About The CampusMart App Project

## Built With
List here all the dependencies of your project (including version). For example:

* [Python](https://www.python.org/downloads/release/python-3127/) v3.12.7
* [Django](https://www.djangoproject.com/) v5.1.7 (but should still work on the student machines - Django v5.0.6)
* [Bootstrap](https://getbootstrap.com) v5.3.0

## Getting Started
To get a local copy up and running follow these simple steps.

### Prerequisites
* Python: install Python v3.12.7 using the link above
* Django: install pip by following directions [here](https://pip.pypa.io/en/stable/installation/), 
    * then ensure pip is installed by running  
        ```sh
        pip --version
        ```
    * then to install the Django version we used, run
        ```sh
        pip install Django==5.1.7
        ```

### Installation
1. Ensure you have all the dependencies described above (Python, Django, Bootstrap) installed.
2. Clone the repo
   ```sh
   git clone git@github.com:sjacobo3/Paradigms_SP25_Course_Project.git
   ```
3. Deploy the website by running the line below, while you are in the Paradigms_SP25_Course_Project/src/course_project/ directory
    ```sh
    python3 manage.py runserver
    ```
4. Click on the url it gives you

### Organization
* src/course_project/
* -> campusmart/
* ->-> migrations/: includes migrations of our app models
* ->-> static/campusmart/: includes campusmart logo and css stylesheet for base.html
* ->-> templates/campusmart/: includes all the template html files used for website rendering
* ->-> utils/campusmart/: includes api_helpers.py file used for API requests in Feature 4.1
* ->-> __init__.py
* ->-> admin.py
* ->-> apps.py
* ->-> models.py: includes the declaration of our models and their attributes
* ->-> tests.py
* ->-> urls.py: includes the url mappings for our app
* ->-> views.py: includes the view functions for our app
* -> course_project/
* ->-> __init__.py
* ->-> asgi.py
* ->-> settings.py: includes the settings for our project
* ->-> urls.py: includes the url mappings for our project
* ->-> wsgi.py
* -> media/listing_photos: shows all uploaded listing images
* -> db.sqlite3: the database for our project
* -> manage.py
* -> .gitignore
* -> CONTRIBUTIONS.MD
* -> Final Report.pdf: our final report
* -> README.MD
* -> requirements.txt
