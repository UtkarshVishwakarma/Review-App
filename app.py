import streamlit as st
from helper import fetch_reviews
from preprocessor import process_text
import pandas as pd
import pickle
import plotly.express as px
from scipy.sparse import csr_matrix
import scipy

model = pickle.load(open('model.pkl', 'rb'))

st.title("IMDB Movie Reviews Sentiment Analyzer")

movie = st.text_input("Search For A Movie")

if st.button("Search"):
    try:
        titles, reviews = fetch_reviews(movie)
        st.markdown("""
        <style>
        .circle-container {
            display: flex;
            align-items: center;
            margin: 10px;
        }

        .circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 12px;
            font-weight: bold;
        }

        .green-circle {
            background-color: green;
            color: white;
        }

        .red-circle {
            background-color: red;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display circles with text
        col1, col2 = st.columns(2)
        with col1:
             st.markdown('<div class="circle-container"><div class="circle green-circle">P</div>Positive</div>', unsafe_allow_html=True)
        with col2:
             st.markdown('<div class="circle-container"><div class="circle red-circle">N</div>Negative</div>', unsafe_allow_html=True)
        
        positive = 0
        negative = 0
        for i in range(len(titles)):
            data_titles = process_text(titles[i])[0:8000]
            data_text = process_text(reviews[i])[0:8000]

            if model.predict([data_text])[0] == 0:
                negative = negative+ 1
                color='red'

            else:
                positive = positive+ 1
                color='green'

            st.header(titles[i])
            # Separate review and list items, and apply color to each line
            review_lines = reviews[i].split('\n')
            colored_review = ''
            for line in review_lines:
                colored_line = f'<span style="color: {color};">{line}</span>'
                colored_review += colored_line + '\n'

            st.markdown(colored_review, unsafe_allow_html=True)

        data = {'Variables':['positive', 'negative'], 
                'Value':[positive, negative]
                }
        
        df = pd.DataFrame(data)
        st.table(df)

        fig = px.bar(df ,x='Variables', y='Value', title='Positives & Negatives')
        fig_pie = px.pie(df, values='Value', names='Variables', title='Positives & Negatives')

        st.plotly_chart(fig)
        st.plotly_chart(fig_pie)
    except:
         st.header("Unable To Find The Movie 🤔")