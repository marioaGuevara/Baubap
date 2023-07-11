import streamlit as st
import pandas as pd 
from helpers.auth import check_password

st.set_page_config(layout="wide")

if check_password():
    st.header("Hi!")

    st.write("This is are my answers for the Python and SQL challenges. Hope this makes sense.")
    st.write("You can select either challenge on the left")

    st.subheader("Python Challenge:")
    st.markdown("""
    <p>I have structure the asnwers in the following way:</p>
    <ol>
        <li>
            <p>Insight: I added the insight at top, this way in the second part.</p>
        </li>
        <li>
            <p>Discussion: we can determine the validity of the insight, as I show how I got to it.</p>
        </li>
        <li>
            <p>Business discussion: Let's discuss what this means for our business.</p>
        </li>
    </ol>
    """, unsafe_allow_html=True)

    st.subheader("SQL Challenge:")
    st.markdown("""
    <p>As this is a more staight forward challenge I have structured it this way:</p>
    <ol>
        <li>
            <p>Answer: Where I answer the question of the exercise</p>
        </li>
        <li>
            <p>Query: the query I used to get the result.</p>
        </li>
        <li>
            <p>The result: the table I got in return.</p>
        </li>
    </ol>
    """, unsafe_allow_html=True)
