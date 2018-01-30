# Python Django Application using Docker containers

Most Django applications are built using virtual environments. However, using virtualenv can sometimes cause dependency issues and cause problems while installing packages using “pip”

Docker provides a more efficient and space saving way to run Django applications and deploy them. Docker containers consume lesser space and mitigate the dependencies of a virtual environment.

> To read more about docker, you can visit the official website. [Django Docker Documentation](https://docs.docker.com/compose/django/#connect-the-database)

In this document, we will setup a django application with docker containers.

Docker containers are executable packages, which contains all the code, tools, settings and system libraries to run the project. The code and data persist over longer periods, but the containers themselves are short lived. Storage in docker is achieved via “Volumes”

Volumes are externally mapped storage areas for a container. These can be shared folders on a host (that is your computer), shared drives on network etc.

To run a Django application with docker containers, we need a

* Dockerfile  
* docker-compose.yml file

> Dockerfile automates the build process and is simply a file which the Docker engine understands. The Dockerfile will contain information about the application’s image and this image will be built. Once the image is built, it can be run in a container.

* For our Django app, create a file named “Dockerfile” in the root directory of your project

* Open the Dockerfile and add the below content:

```
FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
```

> As you can observe, the Dockerfile runs on Python 3 (or above)
  * We create a “/code” directory. This directory is created inside the container (similar to how we map files and folders in  virtual machines)
  * The requirements.txt file will be added to the code directory
  * The Docker file will run the “pip install –r requirements.txt” when the image is built first time
  * And the last line, adds all the code in our current directory (“.”) to the “/code/” directory in the container. This will simply copy all our files and folder related to our Django application and make them part of the image to be built.

The next file we need is the docker-compose.yaml file. This file takes care of the services needed for our application to run.

> The docker-compose tool automates building our app’s services all at once  and links them together as described in the docker-compose.yml file

* Create a new file called “docker-compose.yml” and paste the below contents inside:
```
version: '3'
services:
  db:
    image: postgres
    volumes:
          - postgres-data:/var/lib/postgresql/data
  web:
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
volumes:
    postgres-data:
      external: true
```

> * In this file, we provide information about the services needed for our application to Dockerfile
  * In the services, we mention "db" which refers to database. And the image we will be building is postgres.
  * The next service will be "web" (we can name this anything, but we will name it web for convention)
    * Here we provide the command to run the application, the path of the code, port mapping and dependency on database.

Once these files are setup we can simply go ahead and create our first django application.

* Go to the root of the project directory (The same location where you created your Dockerfile and docker-compose.yml file)

* Execute the command to create a new django project using Docker

```
docker-compose run web django-admin startproject efsProj .
```

This will create a new django project, and associate it with the "web" image in the Docker container.

Once a new project is created, go to ```efsProj/settings.py```

Replace the content of Databases with the following:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
Save the file

Now run ```docker-compose up```. This will bring up the containers.

Since our web image depends on the database image "db", both the containers will be bought up together.

You can go to your [localhost](https://localhost:8000) and check that the application is up and running.

You can bring down the containers using the command ``` docker-compose down```

You can make the containers run in the background using ```docker-compose up -d```

At any moment to check the containers running use, ```docker ps```

## Development Instructions:

When you need to run commands with ```manage.py``` during development, you need to preface the ```python manage.py [command]``` with ```docker-compose run web```. This tells Docker to run the command on the web container, which is the main Django app container.
