'''
This module holds classes that represent annotations and
annotated files
'''
import os
import hashlib

def get_file_extension(path):
    '''Returns the extension for a given path'''
    _, extension = os.path.splitext(path)
    return extension

class Annotation(object):
    '''Simple business object wrapping an annotation'''
    field_names = ['file_name', 'start_sec', 'end_sec', 'labels']

    def __init__(self, input_dict):
        # If any of the fields are missing, throw an error
        missing_fields = [
            f for f in Annotation.field_names if not input_dict[f]]
        if any(missing_fields):
            raise ValueError("Missing fields {}".format(missing_fields))

        try:
            self.start_sec = float(input_dict['start_sec'])
        except ValueError:
            raise ValueError("start_sec could not be parsed as number")

        try:
            self.end_sec = float(input_dict['end_sec'])
        except ValueError:
            raise ValueError("start_sec could not be parsed as number")

        self.file_name = str(input_dict['file_name'])
        self.labels = input_dict['labels']

    @property
    def extension(self):
        '''Returns extension for annotation file'''
        return get_file_extension(self.file_name)

    @property
    def unique_filename(self):
        '''Returns a file name based on the hash of the metadata'''
        return "{}{}".format(self.generate_hash(), self.extension)

    def generate_hash(self):
        '''
        Returns a hash based on the annotation metadata so that
        a unique file name can be created that will be the same for
        each annotation
        '''
        hashval = hashlib.md5("{}{}{}{}".format(
            self.file_name, self.start_sec, self.end_sec, self.labels).encode())
        return hashval.hexdigest()

    @property
    def duration(self):
        '''The duration of the annotation'''
        return self.end_sec - self.start_sec

    def to_record(self):
        '''Converts the annotation class to a record'''
        pass


class AnnotatedFile(list):
    '''Simple wrapper to hold all annotations for a given file since a files
    have several annotations associated with them'''

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    @property
    def extension(self):
        '''Returns the extension for the file the annotation is based on'''
        return get_file_extension(self.file_name)
