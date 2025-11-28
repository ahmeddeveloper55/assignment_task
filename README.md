The first thing to do is to clone the repository:

$ git clone https://github.com/xxxxxxxxxxx Thmanyah_assignment_tas
$ cd Thmanyah_assignment_tas


Create a virtual environment to install dependencies in and activate it:

$ pip install --upgrade pip
$ pip install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate


Then install the dependencies:

(venv)$ pip install -r requirements.txt


Note the (venv) in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by virtualenv.
Create a development database:

(env)$ python manage.py migrate


If everything is alright, you should be able to start the Django development server:

(env)$ python manage.py runserver


Open your browser and go to http://127.0.0.1:8000, you will be greeted with a welcome page.
