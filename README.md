# Thmanyah Assignment Task

This repository contains a Django project for the Thmanyah backend assignment.  
The instructions below explain how to set up a local development environment, install dependencies, run database migrations, and start the development server.

---

## 1. Clone the Repository


git clone https://github.com/ahmeddeveloper55/assignment_task.git
cd assignment_task


## 2. Set Up a Virtual Environment
```sh
pip install --upgrade pip
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```




## 3. Install Dependencies
```sh
(venv) pip install -r requirements.txt
```

##4. Apply Database Migrations
```sh
(venv) python manage.py migrate
```

##5. Run the Development Server
```sh
pythosn manage.py runserver
```

##6 Genereate admin user to run api:
```sh
 python manage.py createsuperuser
```

