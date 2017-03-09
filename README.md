# Deep ONC
Deep Neural Network Classification project for Ocean Networks Canada

## Setup

The initial setup of this project is based on a few different technologies:

- [VSCode](https://code.visualstudio.com/) (for Integrated Development Environment)
  - Plugins:  ( Can be installed in VSCode )
    - Docker
    - MagicPython
    - Python
    - Python for VSCode    
- [Docker](https://docs.docker.com/) ( On my Mac I'm using [Docker For Mac](https://docs.docker.com/docker-for-mac/) ) 
- Python: Note you may also need to install python and the python debugging tools on your machine and make sure they are on the path as well

Since this project is currently using docker, a large amount of the setup should be taken care for us by docker.  
This project currently is currently very simple and consists of one python file **app.py**.
The **DockerFile** takes care of grabbing our source code and containerizing it based on the [kaixhin/theano](https://hub.docker.com/r/kaixhin/theano/) image.  This is what allows us to have a minimum amount of setup for our IDE.

## Running

By hitting `F5` **VSCode** will consult the [launch.json](./.vscode/launch.json) and execute any tasks referenced in there.  In this case, we build the docker container using the [Dockerfile.debug](./Dockerfile.debug) which is effectively the same as the Dockerfile with the added installation of the python remote debugging tools via `pip install ptvsd`.  

Therefore, you can set break points within the `app.py` and step through the code which is actually running within the docker container.  

At this point, the `app.py` file does a very simple logistic calculation, but moving forward hopefully this current setup will serve as a platform for future development of Neural Network based classification.

## Documentation

This project uses [GitBook](http://gitbook.io) for building documentation.  If you'd like to build the documentation locally, the easiest way to do so is by doing the following:

- Install gitbook command line tools globally via `npm install -g gitbook-cli`
- from the root of the project run the following commands:
  - `gitbook install`  - Installs all of the plugins for the book
  - `gitbook serve`  - Builds and serves up the documentation through a development server
  - Access the docs at http://localhost:4000

# Future Work

In the near future, I will be exploring developing actual working DNN's for doing classification of whale sounds from the ONC network.

## West Grid
It would be great if we could use docker containers within West Grid as it would speed up deployment / development cycle and increase our effectiveness when developing algorithms.  

