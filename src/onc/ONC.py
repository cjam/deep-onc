import os
import tempfile
import wave
import tensorflow as tf
import pyONC.webservices.oncws as onc
from onc_token import token
import librosa
import csv

class Data:
    AnnotationsFile = os.path.abspath("./src/onc/AllBarkley2014ManualAnnotations_TimeFreq-JASCO_csv.csv")
    CroppedWavsDir = os.path.abspath("./data/onc/cropped_wavs/")
    SamplingRate = 64000

oncArchive = onc.ArchiveFiles(token=token)

def process_annotations(filepath):
    '''
    Reads the annotation file at filepath and passes each annotation
    grouping into buckets based on file
    '''
    file_dict = {}
    with open(filepath) as csv_file:
        fieldnames = ['file_name', 'start_sec', 'end_sec', 'labels']
        annotation_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        next(annotation_reader) # Skip the header
        for annotation in annotation_reader:
            # Get rid of the extra entry if there was one (extra trailing comma in original csv)
            if None in annotation:
                del annotation[None]

            # Since we can have different annotations at different points in the same file
            # create a dictionary of arrays keyed on file name to make download/processing
            # more efficient
            file_name = annotation['file_name']
            if file_name not in file_dict:
                file_dict[file_name] = []

            file_dict[file_name].append(annotation)

    return file_dict

def download_temp_file(filename):
    temp = tempfile.NamedTemporaryFile(suffix=".wav")
    temp.write(oncArchive.getFile(filename=filename))
    return temp

def process_audio_file(annotation, temp_file_path):
    start_sec = float(annotation['start_sec'])
    end_sec = float(annotation['end_sec'])
    file_name = str(annotation['file_name'])
    labels = annotation['labels']
    signal, sample_rate = librosa.core.load(temp_file_path, sr=Data.SamplingRate, offset=start_sec, duration=start_sec-end_sec)
    new_file_name = '{}_{:f}_{:f}.wav'.format(file_name.replace('.wav', ''), start_sec, end_sec)
    output_path = '{}{}'.format(Data.CroppedWavsDir,new_file_name)
    #librosa.output.write_wav()
    print(start_sec, end_sec, sample_rate, file_name, new_file_name, output_path)

def process_sorted_annotations(annotations):
    for filename, annot_list in annotations.items():
        with download_temp_file(filename) as tmp_file:
            for annotation in annot_list:
                process_audio_file(annotation, tmp_file.name)


sorted_annotations = process_annotations(Data.AnnotationsFile)
process_sorted_annotations(sorted_annotations)

# with tempfile.NamedTemporaryFile(suffix=".wav") as temp:
#     start_sec = 
#     end_sec = 
#     labels =
#     temp.write(oncArchive.getFile(filename='ICLISTENHF1251_20140101T000159.729Z.wav'))
#     y, sr= librosa.core.load(temp.name, duration=5, sr=None)
#     librosa.output.write_wav("./test.wav",y,sr) 

print("All Done")






