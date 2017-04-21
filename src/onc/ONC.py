import os
import tempfile
from queue import Queue
from multiprocessing import cpu_count
import threading
import csv
import pyONC.webservices.oncws as onc
from annotations import AnnotatedFile, Annotation
from processors import WavCroppingAnnotationProcessor
import onc_token

class Data(object):
    '''
    The Data class just holds paths and urls to the various data sources
    in addition to a few higher level utilities
    '''
    AnnotationsFile = os.path.abspath(
        "./src/onc/AllBarkley2014ManualAnnotations_TimeFreq-JASCO_csv.csv")
    CroppedWavsDir = os.path.abspath("./data/onc/cropped_wavs/")
    SamplingRate = 64000


class AnnotationFileManager(object):
    '''
    Manages the downloading and processing for annotated files from ONC archive
    '''
    def __init__(self, oncToken, download_threads=0):
        if not oncToken:
            raise onc_token.TokenMissingException()
        self.file_archive = onc.ArchiveFiles(token=oncToken)
        self.processors = []
        self.download_queue = Queue()
        self.process_queue = Queue()
        # If not specified create a thread for each CPU
        # leaving one for processing thread
        self.num_download_threads = cpu_count(
        ) - 1 if download_threads == 0 else download_threads
        self.total_files_to_process = 0
        self.num_files_processed = 0

    def __on_file_processed(self):
        self.num_files_processed += 1
        print("{:.1f}% complete ({} of {})".format(
            (self.num_files_processed / float(self.total_files_to_process)) * 100,
            self.num_files_processed,
            self.total_files_to_process))

    class DownloadThread(threading.Thread):
        '''
        Thread class for downloading files from ONC
        '''

        def __init__(self, thread_id, downloadQueue, processQueue, fileArchive):
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.download_queue = downloadQueue
            self.process_queue = processQueue
            self.file_archive = fileArchive

        def run(self):
            while True:
                annotated_file = self.download_queue.get()
                tmp_file = self.__download_temp_file(annotated_file)
                self.process_queue.put((annotated_file, tmp_file))
                self.download_queue.task_done()

        def __download_temp_file(self, annotated_file: AnnotatedFile):
            print("\nThread #{} downloading {}".format(
                self.thread_id, annotated_file.file_name))
            temp = tempfile.NamedTemporaryFile(suffix=annotated_file.extension)
            temp.write(self.file_archive.getFile(
                filename=annotated_file.file_name))
            print("\nThread #{} finished downloading {}".format(
                self.thread_id, annotated_file.file_name))
            return temp

    class ProcessingThread(threading.Thread):
        '''
        Thread Class for processing annotations
        '''

        def __init__(self, processQueue, processors, on_task_finished):
            threading.Thread.__init__(self)
            self.process_queue = processQueue
            self.processors = processors
            self.on_task_finished = on_task_finished

        def run(self):
            while True:
                annotated_file, tmp_file = self.process_queue.get()
                self.__process(annotated_file, tmp_file)
                if callable(self.on_task_finished):
                    self.on_task_finished()
                self.process_queue.task_done()

        def __process(self, annotated_file: AnnotatedFile, temp_file):
            able_processors = [
                p for p in self.processors if p.can_process(annotated_file)]
            with temp_file:
                print("\nProcessing file {}".format(annotated_file.file_name))
                for annotation in annotated_file:
                    for processor in able_processors:
                        processor.process(annotation, temp_file.name)

    def begin_processing(self):
        '''Begins the processing'''
        print("Beginning annotation processing with:")
        print("{} annotation processors".format(len(self.processors)))
        print("{} Downloading threads".format(self.num_download_threads))
        print("1 Processing Thread")
        print("{} out of {} annotations left to process".format(
            self.total_files_to_process - self.num_files_processed, self.total_files_to_process))
        print("----------------------------------------")

        for processor in self.processors:
            processor.begin_processing()

        # Start downloading threads
        for i in range(0, self.num_download_threads):
            _t = self.DownloadThread(i, self.download_queue,
                                     self.process_queue, self.file_archive)
            _t.setDaemon(True)
            _t.start()

        # Start Processing Thread
        _t = self.ProcessingThread(
            self.process_queue, self.processors, self.__on_file_processed)
        _t.setDaemon(True)
        _t.start()

    def finish_processing(self):
        '''
        Cleans up after the processing is finished
        '''
        self.download_queue.join()
        self.process_queue.join()

        print("Work finished, cleaning up.")
        for processor in self.processors:
            processor.finish_processing()

    def process(self, files_to_process):
        '''
        Takes a list of files to process
        '''
        # if only one annotation is passed in, put it into a list to keep rest
        # of the code the same
        if isinstance(files_to_process, AnnotatedFile):
            files_to_process = [files_to_process]

        self.total_files_to_process = len(files_to_process)
        self.num_files_processed = 0
        for annotated_file in files_to_process:
            # Only add in files that can be processed
            if any(p.can_process(annotated_file) for p in self.processors):
                self.download_queue.put(annotated_file)
            else:
                self.num_files_processed += 1
                print("No processing needed for annotated file {}".format(
                    annotated_file.file_name))

        self.begin_processing()
        self.finish_processing()

    @staticmethod
    def parse_annotations(csv_file_path, skip_first=True):
        '''Opens a file and yields annotations from it optionally skipping the first line'''
        with open(csv_file_path) as csv_file:
            reader = csv.DictReader(
                csv_file, fieldnames=Annotation.field_names)
            line_num = 0
            if skip_first:
                line_num += 1
                next(reader)
            for csv_entry in reader:
                try:
                    # TODO: HANDLE BAD ENTRIES
                    line_num += 1
                    result = Annotation(csv_entry)
                    yield result
                except ValueError as e:
                    print("Corrupt entry detected at line #{} in {}, Error: {}".format(
                        line_num, csv_file_path, e))

    @staticmethod
    def parse_grouped_annotations(csv_file, skip_first=True):
        '''
        Returns a list of AnnotatedFile objects from a csv file
        '''
        # Here we use a dictionary as a lookup to find the AnnotatedFile
        file_dict = {}
        for annotation in AnnotationFileManager.parse_annotations(csv_file, skip_first=skip_first):
            filename = annotation.file_name
            if filename not in file_dict:
                file_dict[filename] = AnnotatedFile(filename)
            file_dict[filename].append(annotation)

        # return a list of AnnotatedFiles
        return [v for v in file_dict.values()]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="The path to the csv file to parse")
    parser.add_argument("-o", "--out-dir", help="The directory to place processed files")
    parser.add_argument("-t","--token", help="ONC Token")
    parser.add_argument("--token-file",help="File with ONC token stored")
    parser.add_argument("--set-token",help="Stores the ONC token", action="store_true")
    
    args = parser.parse_args()

    input_file = args.input_file if args.input_file else Data.AnnotationsFile
    output_dir = args.out_dir if args.out_dir else "./output_dir/"
    token = args.token
    token_file = args.token_file if args.token_file else onc_token.TOKEN_FILE_PATH
    set_token = args.set_token

    if set_token:
        token = onc_token.save_token(token_file)

    if not token:
        token = onc_token.get_token(token_file)

    print("Processing {} into {}".format(input_file, output_dir))

    onc_manager = AnnotationFileManager(token)
    onc_manager.processors.append(
        WavCroppingAnnotationProcessor(os.path.join(output_dir, "cropped_wavs"))
    )

    annotated_files = AnnotationFileManager.parse_grouped_annotations(input_file)
    onc_manager.process(annotated_files)

