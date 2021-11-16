import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import shutil
import os

FOLDER_TO_WATCH = r'C:\myGitRepositories\FolderWatch-using-Python\inbound\\'
OUTPUT = r'C:\myGitRepositories\FolderWatch-using-Python\outbound\\'
ERROR = r'C:\myGitRepositories\FolderWatch-using-Python\error\\'
HISTORY = r'C:\myGitRepositories\FolderWatch-using-Python\processed_history\\'
logging.basicConfig(filename='folder-watch.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        filenames = os.listdir(FOLDER_TO_WATCH)
        logging.info(f'following files detected: {filenames}')
        for filename in filenames:
            if 'file1' in filename:
                shutil.copy(FOLDER_TO_WATCH + filename, HISTORY + filename)
                logging.info(f'File {filename} copied to processed_history folder')
                shutil.move(FOLDER_TO_WATCH + filename, OUTPUT + filename)
                logging.info(f'File {filename} copied to output folder')
            else:
                shutil.move(FOLDER_TO_WATCH + filename, ERROR + filename)
                logging.info(f'File {filename} copied to error folder')

        logging.info('All files processed successfully')


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_TO_WATCH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(3)
            logging.info('Folder is currently empty')
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
