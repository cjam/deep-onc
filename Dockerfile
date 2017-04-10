FROM floydhub/dl-docker:cpu
ARG KERAS_VERSION=2.0.2
ARG TENSORFLOW_VERSION=1.0.1
ARG TENSORFLOW_ARCH=cpu

# Setup some volumes for notebooks, datasets and tensorboard logs
VOLUME /notebooks
VOLUME /tensorboard

# Install GraphViz and pydot and upgrade Tensorflow and Keras
RUN apt-get install -y graphviz \
	&& pip --no-cache-dir install pydot-ng \
	&& pip --no-cache-dir install --upgrade \
	https://storage.googleapis.com/tensorflow/linux/${TENSORFLOW_ARCH}/tensorflow-${TENSORFLOW_VERSION}-cp27-none-linux_x86_64.whl \
	&& pip --no-cache-dir install --upgrade git+git://github.com/fchollet/keras.git@${KERAS_VERSION} \
	&& pip --no-cache-dir install tflearn

# Replace the Jupyter config with our own pointing jupytr at our notebooks volume
COPY jupyter_notebook_config.py /root/.jupyter/
RUN chmod 700 "/root/run_jupyter.sh"

# Expose ports for Tensorboard and Jupyter
EXPOSE 6006
EXPOSE 8888
ENTRYPOINT ["/root/run_jupyter.sh","--no-browser","--notebook-dir","/notebooks"]
