import os
import csv
import pandas as pd
import numpy as np
from timeit import default_timer as timer
from tqdm import tqdm
from gensim import corpora,models,similarities

#Global Paths
interim_directory_path = '/Users/colinsalama/metis/metis-projects/project-4/data/interim/'
save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
processed_data_directory='/Users/colinsalama/metis/metis-projects/project-4/data/processed/'

def build_similarities(n_best=5):
    bowpath = os.path.join(processed_data_directory,'final_bow.mm')
    dictpath = os.path.join(processed_data_directory,'final_dict.dict')

    print('Loading Corpus and Dict.',end='\n\n')
    corpus = corpora.mmcorpus.MmCorpus(bowpath)
    dict = corpora.dictionary.Dictionary.load(dictpath)

    #Build our TF-IDF Model
    print('Building our TF-IDF Model.',end='\n')
    start = timer()
    tfidf = models.TfidfModel(tqdm(corpus),smartirs='ntc')
    print(f'Built our TF-IDF Model in {timer()-start} seconds.')

    print('Saving our TF-IDF Model.')
    start = timer()
    tfidf.save(os.path.join(processed_data_directory,'tfidf_model'))
    print(f'Saved our TF-IDF Model in {timer()-start} seconds.')

    #Use Similarity to find the n_best similar documents
    print('Initializing our new Similarity Matrix.',end='\n')
    start = timer()
    sim = similarities.docsim.Similarity('/Users/colinsalama/metis/metis-projects/project-4/data/processed/shards/shardx',tqdm(tfidf[corpus],leave=False,position=0),num_features=len(dict),num_best=n_best+1,shardsize=524288)
    print(f'Initialized our Similarity Matrix in {timer()-start} seconds.')

    #Save our Similarity Matrix
    print('Saving our Similarity Matrix.')
    start = timer()
    sim.save(os.path.join(processed_data_directory,'similarity_matrix_x'))
    print(f'Similarity Matrix saved in {timer()-start} seconds.')

    return None


def build_bow():
    filepath = os.path.join(interim_directory_path,'combined_partitions.csv')
    tokens = iterTokens(filepath)

    print('Building Dictionary.')
    start = timer()
    simple_dict = corpora.Dictionary(tqdm(iterable=tokens,total=7503950))
    print(f'Build Dictionary in {timer()-start} seconds',end='\n\n')

    print('Saving Dictionary.')
    start = timer()
    simple_dict.save(os.path.join(processed_data_directory,'final_dict.dict'))
    print(f'Saved Dictionary in {timer()-start} seconds',end='\n\n')

    print('Building BoW.')
    start = timer()
    simple_bow = [simple_dict.doc2bow(doc) for doc in tqdm(iterable=tokens,total=7503950)]
    print(f'Built BoW in {timer()-start} seconds.',end='\n\n')

    print('Saving BoW.')
    start=timer()
    corpora.MmCorpus.serialize(os.path.join(processed_data_directory,'final_bow.mm'),simple_bow)
    end = timer()
    print(f'Saved BoW in {timer()-start} seconds',end='\n\n')

    return None

class iterTokens(object):
    def __init__(self,filepath):
        self.filepath = filepath

    def __iter__(self):
        with open(self.filepath) as input_csv:
            reader = csv.reader(input_csv,delimiter=',')
            for row in reader:
                yield row

########################
#Below code was deprecated
########################

#def BuildBOW(save=True):
#    save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
#    title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
#    processed_data_directory='/Users/colinsalama/metis/metis-projects/project-4/data/processed/'
#
    # print('Building Dictionary and Bag of Words objects.',end='\n')
    # wikidict = corpora.Dictionary()
    # bow_corpus = BoWCorpus(save_directory_path, title_directory = title_directory_path, dictionary=wikidict)  # memory friendly
    # print('')
    #
    # if save:
    #     print('Creating and saving dict, corpus and titles.',end='\n')
    #     start = timer()
    #     corpora.MmCorpus.serialize(os.path.join(processed_data_directory,'bow_corpus.mm'), bow_corpus)
    #     end = timer()
    #     t = (start-end)/60
    #     print(f'Building our corpus took {t} minutes.')
    #
    #     start = timer()
    #     wikidict.save(os.path.join(processed_data_directory,'wikidict.dict'))
    #     end = timer()
    #     print(f'Building our dictionary took {start-end} seconds.')
    #
    #     bow_corpus.titles.squeeze().to_csv(os.path.join(processed_data_directory,'titles.csv'))
    # print('All done!')
    #

# def BuildSimilarities(save=True,n_best=5):
#     save_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/partitions/'
#     title_directory_path='/Users/colinsalama/metis/metis-projects/project-4/data/interim/titles/'
#     processed_data_directory='/Users/colinsalama/metis/metis-projects/project-4/data/processed/'
#
#     #Build our Bag of Words and Dictionary
#     print('Building Dictionary and Bag of Words objects.',end='\n')
#     wikidict = corpora.Dictionary()
#     bow_corpus = BoWCorpus(save_directory_path, title_directory = title_directory_path, dictionary=wikidict)  # memory friendly
#     print('')
#
#     if save:
#         print('Saving title objects.',end='\n')
#         wikidict.save(os.path.join(processed_data_directory,'wikidict.dict'))
#         corpora.MmCorpus.serialize(os.path.join(processed_data_directory,'bow_corpus.mm'), bow_corpus)
#         bow_corpus.titles.squeeze().to_csv(os.path.join(processed_data_directory,'titles.csv'))
#
#     #Build our TfidfModel
#     print('Building our TfidfModel.',end='\n')
#     tfidf = models.TfidfModel(bow_corpus,smartirs='ntc')
#     print('')
#
#     if save:
#         print('Saving title objects.',end='\n')
#         #wikidict.save(os.path.join(processed_data_directory,'wikidict.dict'))
#         #corpora.MmCorpus.serialize(os.path.join(processed_data_directory,'bow_corpus.mm'), bow_corpus)
#         bow_corpus.titles.squeeze().to_csv(os.path.join(processed_data_directory,'titles.csv'))
#
#     #Use SparseMatrixSimilarity to find the n_best similar documents (excluding the first one which is the same as the input)
#     print('Initializing our Similarity Matrix.',end='\n')
#     sim = similarities.docsim.SparseMatrixSimilarity(tfidf[bow_corpus],num_features=len(wikidict),num_best=n_best+1)
#     print('')
#
#     #Build our n best for all documents and save as a numpy array of lists to be loaded later
#     print('Building our Similarity Matrix.',end='\n')
#     all_similarities = np.asarray(sim[bow_corpus][1:n_best])
#     print('')
#
#     if save:
#         print('Saving our Similarity Matrix.',end='\n')
#         np.save(os.path.join(processed_data_directory,'similarity_matrix.npy'), all_similarities)
#     return None
#
# class BoWCorpus(object):
#     """ Iterator for Gensim to go through every line and every file. """
#     def __init__(self,directory_name,title_directory,dictionary):
#         self.directory_name = directory_name
#         self.dictionary = dictionary
#         self.title_directory = title_directory
#         self.titles = pd.DataFrame()
#
#     def __iter__(self):
#         global wikidict
#         #files = 0
#         #limit = 600
#         #t_1 = tqdm(desc='All Files',total=len(os.listdir(self.directory_name)))
#         i=0
#         for file in os.listdir(self.directory_name):
#
#             #j = 0
#             #Drop the first element of the title dataframe because it is empty
#             title_df = pd.read_csv(os.path.join(self.title_directory,file),names=['article_name']).drop(axis=0,index=0)
#             if self.titles.empty:
#                 self.titles = title_df
#             else:
#                 #Join the next title df on top of the other
#                 self.titles = pd.concat([self.titles,title_df],axis=0).reset_index(drop=True)
#             #Open and yield the row
#             temp_path = os.path.join(self.directory_name,file)
#             #t_2 = tqdm(desc='Intra-File',total=os.stat(temp_path).st_size,leave=True)
#             with open(temp_path) as input_csv:
#                 reader = csv.reader(input_csv,delimiter=',')
#                 for row in reader:
#                     bow = self.dictionary.doc2bow(row,allow_update=True)
#                     #Build the dictionary each word at a time
#                     wikidict.merge_with(self.dictionary)
#                     yield bow
#                     #j += 1
#                     #if j > limit:
#                     #    break
#                     #row_size = row.__sizeof__()
#                     #t_2.update(row_size)
#             #t_2.close()
#             #t_1.update()
#             i += 1
#             if i >= 1:
#                 break
#         #t_1.close()
#
#
#     def emptyTitles(self):
#         self.titles = pd.DataFrame()
#         return None
