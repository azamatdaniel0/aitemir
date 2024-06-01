aitemir
This repository contains the code for the aitemir project.

Getting Started
To get started with this project, follow the instructions below to set up and run the application using Docker.

Prerequisites
Make sure you have the following installed on your system:

Docker
Docker Compose
Installation
Clone the repository

git clone https://github.com/azamatdaniel0/aitemir.git
cd aitemir

docker compose up -d --build
Run database migrations

docker compose exec web python3 manage.py makemigrations
docker compose exec web python3 manage.py migrate
Usage
Once the containers are up and the migrations are run, you can access the application through the web interface.

Stopping the Application
To stop the running containers, use:

docker compose down
Additional Commands
To view the logs of the running containers:

docker compose logs
To access the web container's shell:
docker compose exec web /bin/bash
Contributing
If you wish to contribute to this project, please follow the standard GitHub flow:

Fork the repository.
Create a new branch.
Make your changes.
Submit a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

