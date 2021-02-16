# superset-docker-install
alternative superset docker-based installation

Apache superset comes with a docker-based installation
The docker-compose.yaml file contains several dockers including node, worker, db (postgres), cache (redis) and etc. 
The depends on the node.js seems to be unncessary and make it easier to break. 
We create an alternative DockerFile and docker-compose file with PyPi superset package as base. 
This has two benefits: 1) no dependency on Node.js, 2) no need to install Apache Superset Source code, once can quickly switch between different versions available from PyPI
