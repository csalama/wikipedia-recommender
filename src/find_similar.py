import os
import streamlit as st
import pandas as pd
from gensim import similarities

#Global Paths
processed_data_directory='/Users/colinsalama/metis/metis-projects/project-4/data/processed/'
interim_directory_path = '/Users/colinsalama/metis/metis-projects/project-4/data/interim/'

def find_similar_articles(article_name):
    #Load titles dictionary
    tid = titles_to_id()
    #Check if the article exists
    if article_name not in tid:
        return None
    #Load similarity array
    sim = similarities.docsim.Similarity.load(os.path.join(processed_data_directory,'similarity_matrix_x'))
    #Find article number
    article_number = tid[article_name]
    #Use similarity_by_id
    similar_articles = sim.similarity_by_id(article_number)
    idt = id_to_titles()
    return [idt[article_id] for article_id,similarity in similar_articles][1:]

def titles_to_id():
    titles = pd.read_csv(os.path.join(interim_directory_path,'combined_titles.csv'))
    return titles.set_index('article_name').squeeze().to_dict()

def id_to_titles():
    titles = pd.read_csv(os.path.join(interim_directory_path,'combined_titles.csv'))
    return titles.drop('Unnamed: 0',axis=1).squeeze().to_dict()
