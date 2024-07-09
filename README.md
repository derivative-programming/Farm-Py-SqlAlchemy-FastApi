# Python 3.11 SqlAlchemy FastAPI

## Intro

This repo is holding an example of a sqlalchemy\fastapi application. This source code is used to create templates for the source code generator used by  https://github.com/derivative-programming/ModelWinApp and https://secure.derivative-programming.com

Addition of features to this repo adds features to source code generated by the deriviative-programming domains services.
  
##todo
handle if column is encrypted. (done?)
file upload
stream out if objwf output param is set to stream out 
cache lookups. individual ones? in memory? by code? by id? lookups only? not during testing
issue on organization tests on  build org_custome. same for org_api_key.  they are intersection tables.
stress tests

## Tech Used 
SqlAlchemy
pydantic
FastApi
linters (flake8,pylint,sonarlint)
docker
pytest (with coverage.py, using sqlite)
sonarqube



## notes
defaults to local SqlLite db
tests use sqllite im-memory db
models: usual orm stuff
reports: for queries across models. Pagenated, searchable,
managers: controllers to access models
business: uses model instances and reports to give enhanced features
flows: holds business logic. format [owner model name].[business flow name]
apis: endpoints to access reports and flows

Install python

Update pip...
>python.exe -m pip install --upgrade pip

start virtual env...
env\scripts\activate

Install requirements...
>pip install -r requirements.txt

linter notes...
Some rules were excluded in some lines and\or files, particularly in test files


test...
pytest
test and show all...
pytest -v --alluredir=allure-results
docker run -d -p 4040:4040 -v ${PWD}\allure-results:/app/allure-results -v ${PWD}\allure-report:/app/allure-report frankescobar/allure-docker-service
http://localhost:4040

test with coverage report...
coverage run -m pytest
coverage report    ...# for a simple report
coverage html ...# for a larger report

test with sqlite on docker...
docker compose -f "docker-compose.sqlite-[db or memory].pytest.yml" up -d --build
allure report: http://localhost:4040
coverage report: http://localhost:8080
view sqlite db: 

for SonarQube Analysis...
1. compose up the file docker-compose.sqlite-memory.pytest.yml and let run
 This will run all tests and generate pylint and coverage reports
2. then, compose up the file docker-compose.sonarqube.yml and let run.
    This will run sonarqube processing and serve it in on a www site
    server: http://localhost:9000


collect requirements...
>pip freeze > requirements.txt
copy requirements.txt requirements.windows.txt
remvoe "pywin32==306" from requirements.txt (this is for windows, not the linux images)

view dependency tree...
pipdeptree > dependencies.txt


run local with sqlite...
uvicorn main:app --reload
http://127.0.0.1:8000

build and run in docker with default sqlite db...
docker build -f Dockerfile.app -t demo_app-image .
docker run -d -p 8000:8000 --name demo_app-container  demo_app-image
http://127.0.0.1:8000/redoc

run docker compose (also available in vs code popup menu with docker extension)
docker-compose up --build -d (build and run detached)
docker-compose up -d (run detached)
docker-compose ps (check status of containers)
docker-compose logs <service-name>
docker-compose down (stop running the containers)

free up docker resources...
docker system prune -a
docker volume prune

open pgadmin on some docker compose (full featured postgres ui)
http://localhost:5050
register db server with hostname as name of db instance in docker-compose (db), since its on the same network

open adminer on some docker compose (simple open db ui)
http://localhost:6060
log in using db credentials. db name is not necessary


## api
/openapi.json
/redoc
 

# Getting Started
Before you can contribute, you'll need to set up a local copy of the repository:

* Fork the repository by clicking on the "Fork" button in the top right corner of the repository page.
* Clone the forked repository to your local machine: git clone https://github.com/YOUR_USERNAME/Farm-Py-SqlAlchemy-FastApi.git
* Navigate to the repository directory: cd Farm-Py-SqlAlchemy-FastApi
* Now you're ready to make changes to the code!

# Making Changes
* Create a new branch for your changes: git checkout -b my-new-branch
* Make your changes to the code.
* Commit your changes: git commit -am "Added a new feature"
* Push your changes to your fork: git push origin my-new-branch

# Creating a Pull Request
* Go to your forked repository on GitHub and click the "New pull request" button.
* Select the branch you just pushed your changes to.
* Give your pull request a meaningful title and description.
* Submit the pull request and wait for a project maintainer to review your changes.
