# Project 4 - Initialization

**-- Project Status: Active**



### Project Intro/Objective

The purpose of this project is to build a recommendation system for similar Wikipedia articles to a single Wikipedia page.



### Project Description

The project will take a Wikipedia article/page as the input and will provide an arbitrary number of the most similar articles as an output.  This project will use topic modeling through SVD and NMF in order to reduce Wikipedia articles to some number of topics, and then will find the most similar articles according to these dimensions. This is the initial plan, but it is subject to change.

Wikipedia allows you to download all articles in text form from [here](https://dumps.wikimedia.org/enwiki/).  A nice tutorial is given [here](https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c) and is relied on for importing data.  Note that Wikipedia includes ~15 GB compressed and ~58 GB uncompressed.  Reducing the dimension of long Wikipedia articles to a variety of topics will help processing time as well as using parralellization.

Wikipedia articles are slightly challenging to parse because it does not contain clean text to model as a book might.  We will clean this using mwparserfromhell, xml.sax, and a WikiXmlHandler function.



### Project Needs - Initial

#### Model Needs

- Need to decide on cleaning method for a Wikipedia article.  Messy text in Wikipedia articles includes different symbols, bracketed text, and others.

- Need to decide on the best way to reduce dimensions of a Wikipedia article.  Likely either SVD or NMF.

- Need to find the most similar articles using some method.  Possibly cosine distance.

  

#### Code Needs

- Build the make_dataset file to import the compressed Wikipedia file.
- Build a cleaning function within util that cleans a Wikipedia article and returns none if it should not be included (e.g. REDIRECT articles)
- Build the build_features file to iteratively decompress Wikipedia articles, reduce dimensions, and save to a pickled dataset within data/iterim.
- Build the train_model file with several options to find the closest Wikipedia article from the reduced dimension articles.  Save this modeled data within data/processed.
- Build predict_model function to use the train model function to simply
- Build some data viz models