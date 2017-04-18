import os
import tempfile
import wave
import tensorflow as tf
import pyONC.webservices.oncws as onc
from onc_token import token
import librosa
import csv


class Data(object):
    '''
    The Data class just holds paths and urls to the various data sources
    '''
    AnnotationsFile = os.path.abspath(
        "./src/onc/AllBarkley2014ManualAnnotations_TimeFreq-JASCO_csv.csv")
    CroppedWavsDir = os.path.abspath("./data/onc/cropped_wavs/")
    SamplingRate = 64000

    # def get_cropped_file_name(annotation):
    #     file_name = annotation['file_name']

    #     new_file_name = '{}_{:f}_{:f}.wav'.format(
    #         file_name.replace('.wav', ''), start_sec, end_sec)
    #     return new_file_name


class Annotation(object):
    '''Simple business object wrapping an annotation'''

    def __init__(self, csv_entry, line_id=-1):
        self.line_id = line_id
        self.start_sec = self.parse_float(csv_entry['start_sec'], 0)
        self.end_sec = self.parse_float(csv_entry['end_sec'], -1)
        self.file_name = str(csv_entry['file_name'])
        self.labels = csv_entry['labels']

    def parse_float(self, val, defaultValue):
        try:
            return float(val)
        except Exception as e:
            return defaultValue

    @property
    def duration(self):
        '''The duration of the annotation'''
        return self.end_sec - self.start_sec

    def to_record(self):
        '''Converts the annotation class to a record'''
        pass

    @staticmethod
    def from_file(filepath, skip_first=True):
        '''Opens a file and yields annotations from it optionally skipping the first line'''
        with open(filepath) as csv_file:
            fieldnames = ['file_name', 'start_sec', 'end_sec', 'labels']
            reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            line_num = 0
            if skip_first:
                next(reader)
            for csv_entry in reader:
                yield Annotation(csv_entry, line_id=line_num)
                line_num += 1


class AnnotatedFile(list):
    '''Simple wrapper to hold all annotations for a given file'''

    def __init__(self, file_name):
        super(self.__class__, self).__init__()
        self.file_name = file_name

    def to_records(self):
        pass

    @staticmethod
    def from_file(filepath, skip_first=True):
        '''Returns a list of AnnotatedFile objects from a csv file'''
        file_dict = {}
        for annotation in Annotation.from_file(filepath, skip_first=skip_first):
            if annotation.file_name not in file_dict:
                file_dict[annotation.file_name] = AnnotatedFile(
                    annotation.file_name)

            file_dict[annotation.file_name].append(annotation)
        return [v for v in file_dict.values()]


oncArchive = onc.ArchiveFiles(token=token)


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def group_annotations(filepath):
    '''
    Reads the annotation file at filepath and passes each annotation
    grouping into buckets based on file
    '''
    file_dict = {}
    for annotation in Annotation.from_file(filepath):
        if annotation.file_name not in file_dict:
            file_dict[annotation.file_name] = []

        file_dict[annotation.file_name].append(annotation)

    return file_dict


def download_temp_file(filename):
    '''
    Downloads a file from the ONC Archive to a temporary file and returns the path
    '''
    temp = tempfile.NamedTemporaryFile(suffix=".wav")
    temp.write(oncArchive.getFile(filename=filename))
    return temp


def process_audio_file(annotation, temp_file_path):
    '''
    Processes a temporary wave file producing a new file that has been cropped
    according to the annotation provided.
    '''
    start_sec = float(annotation['start_sec'])
    end_sec = float(annotation['end_sec'])
    file_name = str(annotation['file_name'])
    duration = end_sec - start_sec
    labels = annotation['labels']
    signal, sample_rate = librosa.core.load(temp_file_path,
                                            sr=Data.SamplingRate,
                                            offset=start_sec,
                                            duration=duration)
    new_file_name = '{}_{:f}_{:f}.wav'.format(
        file_name.replace('.wav', ''), start_sec, end_sec)
    output_path = '{}{}'.format(Data.CroppedWavsDir, new_file_name)

    # librosa.output.write_wav()
    print(start_sec, end_sec, sample_rate,
          file_name, new_file_name, output_path)


def process_sorted_annotations(annotations):
    '''
    Takes a dictionary of annotations keyed on file name so that
    we only need to download each source file once to produce
    the cropped samples.
    '''
    for filename, annot_list in annotations.items():
        with download_temp_file(filename) as tmp_file:
            for annotation in annot_list:
                process_audio_file(annotation, tmp_file.name)


annotatedFiles = AnnotatedFile.from_file(Data.AnnotationsFile)

#sorted_annotations = group_annotations(Data.AnnotationsFile)
# process_sorted_annotations(sorted_annotations)

# with tempfile.NamedTemporaryFile(suffix=".wav") as temp:
#     start_sec =
#     end_sec =
#     labels =
#     temp.write(oncArchive.getFile(filename='ICLISTENHF1251_20140101T000159.729Z.wav'))
#     y, sr= librosa.core.load(temp.name, duration=5, sr=None)
#     librosa.output.write_wav("./test.wav",y,sr)

print("All Done")
