# Northcoders News API


## Project Summary

The back end of a news aggregate website. Serves subpages(topics), posts, users and comments. Consumers of the API can retrieve, post, edit and delete data.

Current features:

- Subpages, users and articles can all be served as arrays
- Post can be sorted by subpage (topics)
- Posts can be served by id
- Posts and Comments can be updated with votes
- Arrays of comments for each post can be served by post id
- Comments can be served by id
- Comments can be created and must be associated with an post id
- Comment can have other Comments as replies
- Comments can be deleted


## Hosted Version

https://reddit-flask-api.herokuapp.com/

## Clone and Install

Clone the repository into a local folder.
` git clone https://github.com/luccacastro/be-nc-news.git

Make sure both Python and Pip is installed up to the required version (see below). Make use of `pip3 -v` if unsure of your current version.

Install `virtualvenv` in order to create a separate pip dependency environment for your project and run `source venv/bin/activate` to activated it.

Afterwards, run `pip install -r requirements.txt` to install all project and development dependencies.

Make sure to create the local databases by running the setup script (`python3 models.py`). Then seed them with data (`python3 seed.py`).

For serving the project just type (`python3 run.py`)

## Local Environment Setup

This is to connect both local and deployed versions of the databases. 

Create a .env file and create the following variables inside :

In `.env`:
- HOST= 
- DBNAME= 
- DBUSER=
- PORT=
- PASSWORD=


## Version Requirements

- Python v3.10
- Pip 20.0.2
- Flask 2.1.1
- Flask-SQLAlchemy 2.5.1
- SQLAlchemy 1.4.33 (Postgres)

## Front End utilising this API