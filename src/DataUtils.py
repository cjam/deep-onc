"""Utilities for downloading and providing datasets"""
import sys
import re
import os
import tensorflow as tf
from six.moves import urllib

NUM_CLASSES = 527

## DOWNLOADING FILES

def progresshook(blocknum, blocksize, totalsize):
    """Just outputs download progress to the console"""
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        output_str = "\r%5.1f%% %*d / %d" % (percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(output_str)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def maybe_download(filename, work_directory, source):
    """Downloads data from a source unless it is already present"""
    print "Looking for data %s in %s" % (filename, work_directory)

    if not os.path.exists(work_directory):
        os.mkdir(work_directory)

    filepath = os.path.join(work_directory, re.sub('.*/)', '', filename))

    if not os.path.exists(filepath):
        if not filename.startswith("http"):
            url_filename = source + filename
        else:
            url_filename = filename
        print 'Downloading from %s to %s' % (url_filename, filepath)
        filepath, _ = urllib.request.urlretrieve(
            url_filename, filepath, progresshook)
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')

    if os.path.exists(filepath):
        print 'Extracting %s to %s' % (filepath, work_directory)
        os.system('tar xf %s -C %s' % (filepath, work_directory))
        print 'Data ready!'
        return filepath.replace(".tar", "")


def read_audioset_tfrecord(filenames, num_classes=NUM_CLASSES):
    '''
    Reads a list of file names as a queue of tfrecords from the audioset dataset
    '''
    tfrecord_file_queue = tf.train.string_input_producer(filenames, name='queue')
    reader = tf.TFRecordReader()
    _, tfrecord_serialized = reader.read(tfrecord_file_queue)

    features, sequence = tf.parse_single_sequence_example(tfrecord_serialized,
                        context_features={
                            'video_id':tf.FixedLenFeature(shape=[], dtype=tf.string),
                            'start_time_seconds':tf.FixedLenFeature(shape=[], dtype=tf.float32),
                            'end_time_seconds':tf.FixedLenFeature(shape=[], dtype=tf.float32),
                            'labels':tf.VarLenFeature(dtype=tf.int64)
                        },
                        sequence_features={
                            'audio_embedding': tf.FixedLenSequenceFeature(shape=[], dtype=tf.string)
                        }, name='features')
    
    labels = tf.sparse_to_indicator(features['labels'],num_classes)
    labels.set_shape([None, num_classes])
    audio = tf.decode_raw(sequence['audio_embedding'], tf.uint8,)
    video_id = features['video_id']
    return video_id, labels, audio
    #return audio, labels, video_id
