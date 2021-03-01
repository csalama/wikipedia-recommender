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
from tqdm import tqdm

#Global Path Variables
interim_directory_path = '/Users/colinsalama/metis/metis-projects/project-4/data/interim/'
save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
processed_data_directory='/Users/colinsalama/metis/metis-projects/project-4/data/processed/'
keras_home = '/Users/colinsalama/.keras/datasets/wiki_parallel/'

def concat_tokens():
    full_list = []
    all_titles = pd.DataFrame()

    print('Joining all rows.')
    start= timer()
    for file in tqdm(os.listdir(save_directory_path)):
        title_df = pd.read_csv(os.path.join(title_directory_path,file),names=['article_name']).drop(axis=0,index=0)
        if all_titles.empty:
            all_titles = title_df
        else:
            #Join the next title df on top of the other
            all_titles = pd.concat([all_titles,title_df],axis=0).reset_index(drop=True)
        with open(os.path.join(save_directory_path,file)) as input_csv:
            reader = csv.reader(input_csv,delimiter=',')
            for row in reader:
                full_list.append(row)
    print(f'Joined all rows in {timer()-start} seconds.', end='\n\n')

    print('Saving the files.')
    start = timer()
    with open(os.path.join(interim_directory_path,'combined_partitions.csv'),mode='w') as output_csv:
        output_writer = csv.writer(output_csv,delimiter=',')
        for row in full_list:
            output_writer.writerow(row)
    all_titles.to_csv(os.path.join(interim_directory_path,'combined_titles.csv'))
    print(f'Saved the files in {timer()-start} seconds.')
    return None

def build_tokens():
    data_paths = [os.path.join(keras_home,file) for file in os.listdir(keras_home)]

    start = timer()

    pool = Pool(processes = 11)
    result = pool.map(clean_partition, data_paths)
    pool.close()
    pool.join()

    print(f'{timer() - start} seconds elapsed.')
    return None


def clean_partition(data_path,article_limit=None):

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
        if not article_limit:
            if len(handler._pages) > article_limit:
                break
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
