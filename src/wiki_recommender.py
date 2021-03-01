import streamlit as st
from find_similar import find_similar_articles

if __name__ == '__main__':
    st.markdown('## Wikipedia Recommender')
    input = st.text_input(label = 'Enter a Wikipedia article:')
    similar_articles = find_similar_articles(input)

    if not similar_articles:
        st.text('Article not found.')
    else:
        st.markdown('Your recommended articles are as follows:')
        for article in similar_articles:
            link = 'https://en.wikipedia.org/wiki/' + article.replace(' ','_')
            st.markdown(f'-[{article}]({link})')
