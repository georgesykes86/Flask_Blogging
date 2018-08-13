# Flask_blog

## Summary

A Flask application that allows users to create profiles, make posts and comment on other peoples posts.

## Running the application

### Pre-requisites

The application has been written using Python 3 and assumes you have Python 3 installed on your hardware. If this is not the case then you will need to update your Python version. You will also need virtualenv although venv should provide the same functionality.

### Installing

First clone the directory using ```git clone https://github.com/georgesykes86/Flask_Blogging.git```

To set up the directory you will need go into the directory from the command line ```cd Flask_Blogging```. Inside the directory run the following commands.

```bash
virtualenv -p python3 <envname>
source <envname>/bin/activate
pip3 install -r requirements.txt
```

### Running the application

The application can be run using the following command which will run the shell script.

```bash
python3 manage.py runserver
```
This should start the server and you will be able to find the server running on localhost:5000

### Running the tests

I used unittest as a testing framework to ensure my application was performing as anticipated. To run the tests use ```python3 manage.py test```

If you want to run code coverage alongside the test suite then use the command ```python3 manage.py test --coverage```

## Methodology

This was a project used to gain familiarity with the Flask microframework. It closely follows the O'Reilly Flask Web Development book by Miguel Grinberg.

## Areas for development

* Improve the test coverage
* Add email confirmation
* Improve the front end styling
* Introduce varied types of media such as posts with images and videos
