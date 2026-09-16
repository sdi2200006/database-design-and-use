# database-design-and-use
Academic database projects covering ER modeling, SQL queries, MySQL, and Python database integration.

## Overview
This repository contains three academic assignments for the course Database Design and Use.
The assignments cover different stages of database development:
- Database modeling and design
- SQL query development
- Python and MySQL integration
  
Together, they demonstrate the progression from designing a relational database to querying it and using it from an application.

## Assignment 1 — Database Design
The first assignment focuses on designing the database for a fictional movie-directing game called Movie Star.
The database was designed using MySQL Workbench and includes entities and relationships for:
- Players
- Directors
- Movies
- Actors
- Countries and cities
- Movie genres
- Scenarios
- Sponsors
- Awards
- Contracts
- Scenery
- Social interactions

The design includes primary keys, foreign keys, and different types of relationships between entities.
Some design choices were documented separately in the project notes.

## Assignment 2 — SQL Queries
The second assignment focuses on writing SQL queries for a movie database.

The queries involve:
- Selecting and filtering data
- Joining multiple tables
- Using nested queries
- Using EXISTS and NOT EXISTS
- Grouping data
- Aggregation
- HAVING
- DISTINCT
- Ordering query results
- Working with relationships between actors, directors, movies, and genres

The assignment includes 10 SQL queries of increasing complexity.

## Assignment 3 — Python and MySQL Application
The third assignment focuses on connecting a Python application to a MySQL database.
The application uses Python for the application logic and executes SQL queries against the database.

The implemented functions include:
- Updating movie rankings
- Finding colleagues of colleagues
- Finding actor pairs based on movie genres
- Selecting the top N actors for each genre
- Querying relationships between actors

The application communicates with MySQL using PyMySQL

## Tools and Technologies
- MySQL
- MySQL Workbench
- SQL
- Python
- PyMySQL
- Relational Database Design
- Modeling
- Database Queries

## What I Practiced
- Designing relational database schemas
- Creating entity-relationship models
- Defining primary and foreign keys
- Modeling one-to-many and many-to-many relationships
- Translating database requirements into relational structures
- Writing SQL queries involving multiple tables
- Using joins, subqueries, aggregation, and grouping
- Working with `EXISTS` and `NOT EXISTS`
- Querying complex relationships between entities
- Connecting Python applications to MySQL databases
- Executing SQL queries from Python
- Processing query results in Python
- Validating user input before database operations

## Project Structure
- ├── README.md
- ├── assignment-1-database-design/
- ├──├── movie-star.mwb
- ├──├── movie-star.sql
- ├──├── notes.md
- ├── assignment-2-sql-queries/
- ├──├── queries.sql
- ├── assignment-3-python-mysql/
- ├──├── app.py

## Assignment 1 
The Movie Star database models a game where players create directors and movies.
Movies can have actors, genres, sponsors, scenarios, scenery, and awards, while directors can gain points and compete for positions in the game ranking.
The database design was created in MySQL Workbench.

## Assignment 2 
The SQL assignment uses a movie database containing tables such as:
- actor
- director
- movie
- genre
- role
- movie_has_genre
- movie_has_director

The queries answer questions involving actors, directors, movie genres, movie years, and relationships between these entities.

## Assignment 3 
The Python assignment is based on a three-tier application architecture:
- Web-based user interface
- Python application logic
- MySQL database

The main implementation is located in app.py, where Python functions execute SQL queries and return the results to the application.

## Security 
Database credentials are not included in this repository.
Before running the Python application, configure your own MySQL connection settings.
