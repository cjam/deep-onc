export VENV_PATH=.env
python3 -m venv $VENV_PATH
source ./$VENV_PATH/bin/activate
# hack because one of the packages imports numpy in its setup
pip install numpy
pip install -r ./requirements.txt