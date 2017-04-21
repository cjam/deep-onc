'''
This module contains various processors that can process annotations
'''
import os
import csv
import librosa
from annotations import AnnotatedFile, Annotation


class AnnotationProcessor(object):
    '''Base Annotation Processor class'''

    def begin_processing(self):
        '''Hook for when processing begins'''
        pass

    def finish_processing(self):
        '''Hook for when processing is finished'''
        pass

    def can_process(self, annotated_file: AnnotatedFile):
        '''
        Returns whether or not the processor can process the given
        AnnotatedFile
        '''
        return True

    def process(self, annotation: Annotation, temp_file_path):
        '''Processes a given annotation using the temp_file_path'''
        pass


class WavCroppingAnnotationProcessor(AnnotationProcessor):
    '''
    Takes annotations and writes out cropped wav files to disk
    '''

    def __init__(self, output_dir="./cropped_wavs/", csv_file_name="cropped_annotations.csv"):
        self.output_dir = output_dir
        self.csv_file_name = csv_file_name
        self._output_csv = None
        self._csv_writer = None

    @property
    def output_csv(self):
        return os.path.join(self.output_dir, self.csv_file_name)

    def __get_output_file(self, annotation: Annotation):
        return os.path.join(self.output_dir, annotation.unique_filename)

    def ensure_directory(self, out_path):
        if not os.path.exists(out_path):
            os.makedirs(out_path)

    def begin_processing(self):
        self.ensure_directory(self.output_dir)
        created = not os.path.isfile(self.output_csv)
        self._output_csv = open(self.output_csv, mode="a+")
        self._csv_writer = csv.DictWriter(self._output_csv, delimiter=',',
                                          fieldnames=['onc_file'] +
                                          Annotation.field_names,
                                          extrasaction="ignore")
        # If we just created the file, then write the header
        if created:
            self._csv_writer.writeheader()

    def finish_processing(self):
        if self._output_csv is not None:
            self._output_csv.close()
            self._output_csv = None
            self._csv_writer = None

    def __write_row(self, annotation, new_file_name):
        if self._csv_writer is not None:
            dict_to_write = dict(annotation.__dict__)
            dict_to_write['onc_file'] = annotation.file_name
            dict_to_write['file_name'] = new_file_name
            self._csv_writer.writerow(dict_to_write)

    def can_process(self, annotated_file):
        files_to_create = [self.__get_output_file(a)
                           for a in annotated_file
                           if not os.path.isfile(self.__get_output_file(a))]
        iswav = str.lower(annotated_file.extension) == ".wav"
        return iswav and len(files_to_create) > 0

    def process(self, annotation, temp_file_path):
        '''
        Crops a given file based on the annotation data, returning the
        signal and sampling rate
        '''
        print("Creating cropped wav file from annotation...", end='')
        duration = None if annotation.end_sec == -1 else annotation.duration
        sig, samp_rate = librosa.core.load(temp_file_path,
                                           sr=None,
                                           offset=annotation.start_sec,
                                           duration=duration)
        new_file_name = "{}{}".format(
            annotation.generate_hash(), annotation.extension)
        new_file_path = os.path.join(self.output_dir, new_file_name)
        self.ensure_directory(self.output_dir)
        librosa.output.write_wav(new_file_path, sig, samp_rate)
        self.__write_row(annotation, new_file_name)
        print("Done")
