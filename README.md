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
- [IPython](https://ipython.org/) which provides a web-based interactive computing shell for creating **notebooks** which are essentially markdown + code that can be executed and have results streamed back to the web.

The majority of the project setup is taken care of by our [DockerFile](./Dockerfile) which is responsible for defining our base image to be used for our environment.  The other component to this setup is the [docker-compose](./docker-compose.yml) file which defines how to spin up the images and wire them together.  We're pulling from this [Deep Learning image](https://github.com/floydhub/dl-docker) and then just upgrading a few packages.

### Docker Compose Structure

Our application consists of two services: 
- **Jupyter**
  - mounts in our `./notebooks` directory within the container at `/notebooks`
  - mounts a shared volume at `/tensorboard` where we will direct tensorflow logs to be processed by the *Tensorboard* service below
  - Starts up the Jupyter service (running on port 8080) and configures it to point at `/notebooks` therefore allowing us to persist our notebooks to disk and thus this repository
- **Tensorboard** 
  - [TensorFlow](https://www.tensorflow.org/) is a deep learning tensor framework that also ships with a visualization platform called [Tensorboard](https://www.tensorflow.org/get_started/summaries_and_tensorboard) 
  - This service takes our base container and mounts a shared volume into `/tensorboard`
  - The Tensorboard service is then started and pointed at the `/tensorboard` location so that logs generated by our *Jupyter* service can be processed and output graphically

> One other Note, if you need a place to put datasets from within your notebooks, use `data/` which in turn will point at `{workspaceRoot}/notebooks/data` which is part of our [.gitignore](./.gitignore) so that it won't be committed but you can still persist it between instances of containers.

## Running

> <span style="color:#339933">I've updated the shell scripts ([dockerTask.sh](./dockerTask.sh)) which work well for *OSX*.</span>

> <span style="color:#993333"> I'm not however on a windows machine so I have neglected fixing up the ([dockerTask.ps1](./dockerTask.ps1)) but it should be straightforward to update it to match the shell script.</span>

In order to get up and running in vscode you will want to do the following:

1. Press `` ctrl+` `` to open up a terminal
2. Type `./dockerTask.sh buildAndCompose`
   - note that the first time that your do this it will take sometime to build the images
3. Open up the Jupyter Application ( [localhost:8888](http://localhost:8888) )
4. Open up the Tensorboard App ( [localhost:6006](http://localhost:6006) )

## Documentation

This project uses [GitBook](http://gitbook.io) for building documentation.  If you'd like to build the documentation locally, the easiest way to do so is by doing the following:

- Install gitbook command line tools globally via `npm install -g gitbook-cli`
- from the root of the project run the following commands:
  - `gitbook install`  - Installs all of the plugins for the book
  - `gitbook serve`  - Builds and serves up the documentation through a development server
  - Access the docs at http://localhost:4000

Now when you modify markdown files within the [docs](./docs) folder the server will automatically refresh your browser with the updated docs.  

### Table of contents

In order to add your page to the table of contents, you must add a link to your page within the [Summary page](./docs/SUMMARY.md) see the [documentation](https://toolchain.gitbook.com/pages.html#summary) for more information.

### Glossary

the [Glossary](./docs/GLOSSARY.md) can be used for defining terms according to [these docs](https://toolchain.gitbook.com/lexicon.html)

### Plugins

Gitbook has many [plugins available](https://plugins.gitbook.com/) which can be installed by adding them to the [book.json](./book.json) file and running `gitbook install` (if building docs locally of course)

Two plugins have been added to the documentation, 
- [Katex](https://github.com/GitbookIO/plugin-katex) which allows for *Latex* to be used within documentation pages.
- [Graph](https://github.com/cjam/gitbook-plugin-graph) A simple plugin that I created for rendering graphs and function plots within a docs page

# Future Work

This project will be using github to track work see:
- [Issues](https://github.com/cjam/deep-onc/issues)
- [Project](https://github.com/cjam/deep-onc/projects/1)

## West Grid
It looks like West Grid supports a containerization framework called [Singularity](http://singularity.lbl.gov/).  

After doing a little digging, it appears that it was designed to handle security in the context of multitenancy on HPC's better than docker's model. It appears that you can create Singularity containers [from Docker containers](http://singularity.lbl.gov/docs-docker) and it will actually pull the file system images down from docker hub.  Pretty cool, will try it once we have more things working.

