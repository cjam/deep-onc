'''
This module is currently for learning purposes
'''
import DataUtils as data
import tensorflow as tf
from os import path

DATA_DIR = "/Users/cmcquay/Documents/School/deep-onc/data/audioset/audioset_v1_embeddings/"

class Data:
    ROOT = DATA_DIR
    URL = "http://storage.googleapis.com/us_audioset/youtube_corpus/v1/features/features.tar.gz"
    CHECKSUM = "cd95d500ab2422d4233cb822e25cf73033633e2068eab64d39024e85125cb760"
    TRAINING_AUDIO_BALANCED = DATA_DIR  + "bal_train/"
    TRAINING_AUDIO_UNBALANCED = DATA_DIR  + "unbal_train/"
    EVALUATION_AUDIO = DATA_DIR + "eval/"
    CLASS_LABELS_URL = "http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv"
    CLASS_LABELS_FILE = DATA_DIR + "dataset-class-labels.csv"

balanced_glob = path.join(path.abspath(Data.TRAINING_AUDIO_BALANCED),"*.tfrecord")

# create our graph
balanced_samples = tf.train.match_filenames_once(pattern=balanced_glob)
video_id, labels, audio = data.read_audioset_tfrecord(balanced_samples)

with tf.Session() as sess:
    tf.global_variables_initializer().run()

    # Coordinate the loading of files
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(10):
        print(sess.run(video_id))
        print(sess.run(audio))
        # print(sess.run(labels))
        # print(sess.run(labels))


    coord.request_stop()
    coord.join(threads)




