import os
import gc
import sys

import csv
import pandas as pd
import xml.sax
import subprocess
import requests

from keras.utils import get_file
from bs4 import BeautifulSoup
from util import cleanWiki, WikiXmlHandler

#save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
#title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
#article_limit=50

def DownloadWikiFile(dateString = '20210201',filename = 'wiki_data',keras_home = '/Users/colinsalama/.keras/datasets/'):
    """ Download the file to your keras_home directory. Around 18 GB download. """
    dump_url = 'https://dumps.wikimedia.org/enwiki/' + dateString
    dump_html = requests.get(dump_url).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')

    #Access the first multistream.xml.bz2 file in the list of links
    url = 'https://dumps.wikimedia.org' + soup_dump.find('li',{'class':'file'}).find('a')['href']
    saved_file_path = get_file(filename,url,cache_subdir=keras_home)


def DownloadParallelWiki(dateString = '20210201',keras_home = '/Users/colinsalama/.keras/datasets/wiki_parallel/'):
    """
    keras_home is the directory you would like to download the parallelized files
    dateString is the dump date that can be found through ListWikiDates.
    returns the list of all data_paths
    """
    dump_url = 'https://dumps.wikimedia.org/enwiki/' + dateString + '/'
    dump_html = requests.get(dump_url).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')
    files = []

    for file in soup_dump.find_all('li', {'class': 'file'}):
        text = file.text
        # Select the relevant files
        if 'pages-articles-multistream' in text:
            files.append((text.split()[0], text.split()[1:]))
    files_to_download = [file[0] for file in files if '.xml-p' in file[0]]

    counter = 0
    data_paths = []
    for file in files_to_download:
        path = keras_home + file

        if not os.path.exists(keras_home + file):
            counter += 1
            current_url = dump_url+file
            #Print out our progress
            print(f'\nDownloading file {counter}')
            print(f'File name: {file}\nDump URL: {current_url}\n')
            data_paths.append(get_file(file,current_url,cache_subdir=keras_home))
    return data_paths

def ListWikiDates():
    """ List all possible date strings available for import from Wikipedia  """
    #Request the dump webpage from Wikipedia
    base_url = 'https://dumps.wikimedia.org/enwiki'
    index = requests.get(base_url).text
    #Analyze the listed links using BeautifulSoup
    soup_index = BeautifulSoup(index, 'html.parser')
    dumps = [a['href'] for a in soup_index.find_all('a') if a.has_attr('href')]
    return dumps
