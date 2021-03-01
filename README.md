<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Alternative Docker Installation for Apache Superset

Docker is an easy way to get started with Superset. 
Apache Superset project has docker build script files that allows one to build docker image directly 
[Apache superset Docker] https://github.com/apache/superset/tree/master/docker
But many times, the image generated show blank page. For first time users, this is not really a good experience.  
The Apache Superset docker-compose.yaml file contains several docker containers
including node, worker, db (postgres), cache (redis) and etc. The dependency on the node.js seems to be unnecessary 
and make it easier to break. I created an alternative Dockerfile and docker-compose file 
with PyPi superset package as base. 

This has the following benefits: 
* no dependency on Node.js, 
* no need to clone Apache Superset Source code
* once can quickly switch between different versions of superset available from PyPI 
   
You still need the same prerequisites before you can use docker installed 
## Prerequisites

1. [Docker!](https://www.docker.com/get-started)
2. [Docker-compose](https://docs.docker.com/compose/install/)

## Build docker image

To build the docker image, simply run:

```bash
docker-compose build  
```
This will genearte the docker images for different containers. In docker-compose file, we have three containers : redis, db and superset with corresponding containers names: superset_cache, superset_db and superset_dev 

```bash
docker-compose up
```
Once superset initialization finished, 
you can open a browser and view [`http://localhost:8088`](http://localhost:8088)

## Trouble Shooting
if the superset did not show up on port 8088, you can debug in the following ways

### Trouble shooting superset database

  start the database first without start superset
  
```Bash
   docker-compose db
```
  "db" here is one the service module defined in docker-compose file. The default database:mySQL 5 is used. 
  You can change to postgres db if you prefer. 
  
  once db started, if you noticed the db container (container name: superset_db) exits with non-zero code,
  that means the database is not starting correctly
  
  In some cases, you might experienced db failed to start with the following error
  
  ```
   [ERROR] --initialize specified but the data directory has files in it. Aborting.
  ```
  the error is misleading, as in most cases, it simply means docker image ran out of disk space. 
  
  running the following command to clear some space seems to work in many cases. 
  
  ```Bash
   docker system prune --volumes     
  ```

  in some cases, you want to re-initialize the database during development, just want to start over.
  you first make sure the docker containers are completely down
  
  you can delete the database files by access the db container 
  
  ```
    docker exec -it superset_db bash
  ```
  once inside the container, go to the mysql data volume and delete the directory
  ```
    rm -r /var/lib/mysql
  ```
  exit the container and completely shut down containers
  
  ```
    docker-compose down
  ``` 
  
   
   
### Trouble shooting superset and other containers

   Similarly you can check each container in the same way. 
   
   ```Bash
     docker-compose up redis
   ```
   redis is the superset cache server. You make sure that it starts correctly
   
   For superset server, you can also starts independently
   
  ```Bash
        docker-compose up superset
  ``` 


   
## Configuration

   The docker-compose parameters can be changed via environment variables
   These includes docker image tag name, database port, superset port, container name etc. 
   once can build different versions of the images based on the deployment env (production, development)
   with different ports. 
   
   In addition, by change SUPERSET_VERSION, you can build different version of superset image.
   The default version is Apache superset 0.34. 
   
   Superset configuration can be changed via superset_config.py 
   
## Note

 * Why default Apache Superset version is 0.34, not 1.0.1 or 1.0 ? 
   That's because I only have the time to tested 0.34 at the moment.
   
 * What about worker containers which leverage celery ?
   in this first version, I did not add worker container
   for local development, we probably don't need it for initial development
   I will add it later if I see the need.   
         
   
