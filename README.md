# Wikipedia Recommender

**-- Project Status: Active**



### Project Intro/Objective

The purpose of this project is to build a recommendation system for similar Wikipedia articles to a single Wikipedia page.

### Project Description

The project will take a Wikipedia article/page as the input and will provide an arbitrary number of the most similar articles as an output.  The initial model used will be a TF-IDF model from the cleaned Wikipedia article introduction.  Then the cosine similarities will be taken to find the top 10 similar articles.  

Wikipedia allows you to download all articles in text form from [here](https://dumps.wikimedia.org/enwiki/).  A nice tutorial is given [here](https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c) and is relied on for importing data in a partitioned form in order to use multiprocessing.  Note that Wikipedia includes ~15 GB of data compressed and ~58 GB uncompressed.  After tokenizing the data, the data is converted into a Gensim Corpus and Dictionary, then converted into TF-IDF file.  Then the Gensim Similarity matrix is created and queried from the Streamlet App.

Future work will involve expanding the recommendation system to implement LDA and Word2Vec, and speeding up the recommendation by storing it in memory. 

### Project Needs

- Update build_similarities.py with LDA and Word2Vec models, and build functions to find similarities off of this.
- Speed up the recommendation system by storing the recommendations into memory.
- Add the Cosine similarity percentage as an output to the Streamlit app.











