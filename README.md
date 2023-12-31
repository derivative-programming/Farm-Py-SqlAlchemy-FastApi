# Python 3.11 SqlAlchemy FastAPI

## Intro

This repo is holding an example of a djnago application. This source code is used to create templates for the source code generator used by  https://github.com/derivative-programming/ModelWinApp and https://secure.derivative-programming.com

Addition of features to this repo adds features to source code generated by the deriviative-programming domains services.
  
##todo
handle if column is encrypted. 
stream out if objwf output param is set to stream out 
cache lookups. individual ones? in memory? by code? by id? lookups only? not during testing
issue on organization tests on  build org_custome. same for org_api_key.  they are intersection tables.

## Tech Used 
SqlAlchemy
pydantic
FastApi

## notes
defaults to local SqlLite db
tests use sqllite im-memory db
models: usual orm stuff
reports: for queries across models. Pagenated, searchable,
managers: controllers to access models
business: wraps model instances to give enhanced features
flows: holds business logic. format [owner model name].[business flow name]
apis: endpoints to access reports and flows

Install python

Update pip...
>python.exe -m pip install --upgrade pip

Install requirements...
>pip install -r requirements.txt

test...
pytest

run...
uvicorn main:app --reload

collect requirements...
>pip freeze > requirements.txt


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
* Commit your changes: git commit -am "Added some new feature"
* Push your changes to your fork: git push origin my-new-branch

# Creating a Pull Request
* Go to your forked repository on GitHub and click the "New pull request" button.
* Select the branch you just pushed your changes to.
* Give your pull request a meaningful title and description.
* Submit the pull request and wait for a project maintainer to review your changes.

