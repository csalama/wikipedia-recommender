#Goal:
# - Convert the raw wikipedia files into the Gensim Bag of Words and Word2ID
# - Save these files into our iterim_data folder

import os
import gc
import sys

import csv
import pandas as pd
import xml.sax
import subprocess
import requests

from util import cleanWiki, WikiXmlHandler
from multiprocessing import Pool
from timeit import default_timer as timer

def BuildTokens():
    keras_home = '/Users/colinsalama/.keras/datasets/wiki_parallel/'
    data_paths = [os.path.join(keras_home,file) for file in os.listdir(keras_home)]

    start = timer()

    pool = Pool(processes = 11)
    result = pool.map(CleanPartition, data_paths)
    pool.close()
    pool.join()

    end = timer()
    print(f'{end - start} seconds elapsed.')
    return None

#def build_test_partition():
#    keras_home = '/Users/colinsalama/.keras/datasets/wiki_parallel/'
#    data_paths = [os.path.join(keras_home,file) for file in os.listdir(keras_home)]
#
#    start = timer()
#    for path_i in data_paths[:10]:
#        CleanPartition(path_i)
#    end = timer()
#    print(f'{end - start} seconds elapsed.')
    #removeInterimFiles()
#    return None

#def build_test_partition_multi():
#    keras_home = '/Users/colinsalama/.keras/datasets/wiki_parallel/'
#    data_paths = [os.path.join(keras_home,file) for file in os.listdir(keras_home)]
#
#    start = timer()
#
#    result = pool.map(CleanPartition, data_paths[:10])
#    pool.close()
#    pool.join()
#
#    end = timer()
#    print(f'{end - start} seconds elapsed.')
#    #removeInterimFiles()
#    return None

def CleanPartition(data_path):
    save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
    title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
    article_limit=50

    #print('Entering CleanPartition function.')
    # Object for handling xml
    handler = WikiXmlHandler()
    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    # Iteratively process file
    for line in subprocess.Popen(['bzcat'],
                                  stdin = open(data_path),
                                  stdout = subprocess.PIPE).stdout:
        parser.feed(line)

        # Stop when article_limit number has been found
        #if len(handler._pages) > article_limit:
        #    break
    p_str = data_path.split('-')[-1].split('.')[-2]
    out_dir = save_directory_path + p_str + '.csv'
    with open(out_dir,mode='w') as output_csv:
        writer = csv.writer(output_csv,delimiter=',',)
        for tokens in handler._pages:
            writer.writerow(tokens)
    titles = pd.DataFrame(handler._titles)
    titles.to_csv(title_directory_path + p_str + '.csv',index=False)

    print(f'{len(os.listdir(save_directory_path))} files processed!',end = '\r')

    del handler
    del parser
    gc.collect()
    return None

#def removeInterimFiles():
#    save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
#    title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
#    for file in os.listdir(save_directory_path):
#        os.remove(os.path.join(save_directory_path,file))
#    for file in os.listdir(title_directory_path):
#        os.remove(os.path.join(title_directory_path,file))
#    return None
