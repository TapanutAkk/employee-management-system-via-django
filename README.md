# Setup Project
## Build and turn on Virtual Environment (venv)
```bash
python3 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process # If it ask you, please type Y. If you can't activate 
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate  # for Windows
```
## Build migration file and migrate database
```bash
python manage.py makemigrations management_api
python manage.py migrate
```
## Create superuser
```bash
python manage.py createsuperuser
# key in username, email, password
```
## Run Server
```bash
python manage.py runserver
```
## Open browser
```bash
http://127.0.0.1:8000/admin/
# Log in with superuser
```
## Run testing
```bash
python manage.py test management_api
```