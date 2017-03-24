imageName="deep-onc"
projectName="deeponc"
composeFileName="docker-compose.yml"

# Kills all running containers of an image and then removes them.
cleanAll () {
  if [[ ! -f $composeFileName ]]; then
    echo "File '$composeFileName' does not exist."
  else
    docker-compose -f $composeFileName -p $projectName down --rmi all
    # Remove any dangling images (from previous builds)
    danglingImages=$(docker images -q --filter 'dangling=true')
    if [[ ! -z $danglingImages ]]; then
      docker rmi -f $danglingImages
    fi
  fi
}

# Builds the Docker image.
build () {
  if [[ ! -f $composeFileName ]]; then
    echo "File '$composeFileName' does not exist."
  else
    echo "Building the image $imageName."
    docker-compose -f $composeFileName -p $projectName build
  fi
}

# Runs docker-compose.
compose () {
  if [[ ! -f $composeFileName ]]; then
    echo "File '$composeFileName' does not exist."
  else
    echo "Running compose file $composeFileName"
    docker-compose -f $composeFileName -p $projectName kill
    docker-compose -f $composeFileName -p $projectName up
  fi
}

# Shows the usage for the script.
showUsage () {
  echo "Usage: dockerTask.sh [COMMAND]"
  echo ""
  echo "Commands:"
  echo "    build:      Runs docker-compose build."
  echo "    compose:    Kills existing running containers and runs docker-compose up"
  echo "    clean:      Removes the image '$imageName' and kills all containers based on that image."
  echo "    buildAndCompose: Runs docker-compose build followed by docker-compose up"
  echo ""
  echo "Example:"
  echo "    ./dockerTask.sh build"
  echo ""
  echo "    This will:"
  echo "        Build a Docker image named $imageName"
}

if [ $# -eq 0 ]; then
  showUsage
else
  case "$1" in
    "compose")
            compose
            ;;
    "buildAndCompose")
            build
            compose
            ;;
    "build")
            build
            ;;
    "clean")
            cleanAll
            ;;
    *)
            showUsage
            ;;
  esac
fi