## Introduction

Built off of a django boilerplate, this repo extends the idea of a classic TODO app as it encompasses the full CRUD functionality required. 

## Requirements
* Python3
* Pipenv

## Getting started

1. Source the virtual environment ```[pipenv shell]```
2. Install the dependencies ```[pipenv install]```
3. Navigate into the frontend directory ```[cd frontend]```
4. Install the dependencies ```[npm install]```

## Run the application
You will need two terminals pointed to the frontend and backend directories to start the servers for this application.

1. Run this command to start the backend server in the ```[backend]``` directory: ```[python manage.py runserver]``` (You have to run this command while you are sourced into the virtual environment)
2. Run this command to start the frontend development server in the ```[frontend]``` directory: ```[npm install]``` (This will start the frontend on the address [localhost:3000](http://localhost:3000))

## Bringing the code to production
This code encompasses the backend for a larger system, in the diagram below I have set out the architecture that could be used to create an enterprise ready system that meets all the needs of a high availability and low latency web app

![Alt text](DudeWheresMyLambo.Architecture.png?raw=true "Title")

