
# coding: utf-8

# In[2]:


'''
This script watches a specified directory for changes. 
As soon as a new file is added to the folder it starts processing it
and saves the output file in the same folder. This script can be run 
automatically using Windows Task Scheduler as well.
'''
#------------------------ Importing libraries-------------------------------------------
import time # For delay in time
import pandas as pd # Pandas library for data analysis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#-------------------------Folder location and file name----------------------------------------------
folder_to_watch='C:/Users/Mohsin Asif/file_processor/'
input_file_name='input.xlsx'  # Specify the file name including the extension i.e. "input.xlsx"
output_file_name='output.xlsx'
#-------------------------Code------------------------------------------------------------------------
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        xl_file=pd.read_excel(folder_to_watch+input_file_name) # Reading the Excel file
        #xl_file=pd.read_csv(folder_to_watch+file_name)  # To read CSV files, uncomment the line
###+++++++++++++++++++++++Specify the processing here:++++++++++++++++++++++++++++++++++++++++++++++++
        sum=xl_file['Sales'].sum()
        xl_file['Percentage of Total Sales']=""
        for value in range(0,len(xl_file['Sales'])):
            xl_file['Percentage of Total Sales'][value]=(xl_file['Sales'][value]/sum)*100
        xl_file.to_excel(folder_to_watch+output_file_name) # Writing Excel file
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++###

#-------------------Generic Watchdog library code----------------------------------------------------
event_handler = MyHandler()
observer = Observer()
#--------------------------------------Specify path to the folder to be watched here-----------------
observer.schedule(event_handler, path=folder_to_watch, recursive=True)
observer.start()
try:
    while True:
        time.sleep(10) # Checking folder after every 10 seconds
except KeyboardInterrupt:
    observer.stop()
observer.join()


