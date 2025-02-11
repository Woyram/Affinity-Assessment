# Affinity-Assessment


## Overview
This is a Flask-based web application that runs inside a Docker container. The application leverages Docker for a consistent development and deployment environment.


## Database Dump
The db_dump directory contains the database dump of the application. This can be used to restore the database when setting up the application.

## Getting Started
#### 1. Clone the Repository
```
git clone https://github.com/Woyram/Affinity-Assessment.git
cd Affinity-Assessment
```

#### 2. Restore the database dump.
```
mysql -u root -p affinity < affinity.sql
```

#### 3. Build and run docker container.
```
docker compose up -d
```

#### 4. Accessing the application
```
http://localhost:8094
```

#### 5. Credentials for application
```
Username: Affinity
Password: Password@1
```
