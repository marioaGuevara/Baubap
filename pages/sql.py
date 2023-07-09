import streamlit as st
import pandas as pd
import gdown
import sqlite3
from helpers.queries import query1, query2, query3,query4
# url = 'https://drive.google.com/uc?export=download&id=1Wq0TQJAgy25FnVRQq9uu-lL3ko281baa'
output = 'Baubap Mysql Challenge'
# gdown.download(url, output, quiet=False)
db_data = pd.read_csv(output)
st.set_page_config(layout="wide")

DB = sqlite3.connect("BAUABAP CHALLENGE.db")
db_cursor = DB.cursor()
# db_data.to_sql(name= "loans",con=DB)

t1, t2, t3 = st.tabs(['Exercise 1', 'Exercise 2', 'Exercise 3'])

with t1:
    st.header("Answer")
    declinedDf = pd.read_sql_query(con=DB,sql=query1)

    aprilDecline = declinedDf.loc[declinedDf['MONTH'] == '2019-04-01'].DECLINED_LOANS_PERC[0]
    marchDecline = declinedDf.loc[declinedDf['MONTH'] == '2019-03-01'].DECLINED_LOANS_PERC[1]
    st.metric('Decline Rate: April, 2019', "{0:.2%}".format(round(aprilDecline,4)), str(round((aprilDecline-marchDecline)*100,2))+"bps MoM", delta_color="inverse")
    
    st.subheader("Here's the query I used")
    st.write("I could've used an interval to make it dynamic, however for our purposes, this seems good.")
    st.code(query1)
    st.subheader("The result I got")
    st.write(declinedDf)

# 
with t2:
    st.code(query2)

    st.write(pd.read_sql_query(con=DB,sql=query2))

with t3: 
    st.header('I wanted to see if there was a correlation between loan amount and the payment likelyhood')
    st.subheader("So first I ran this query to find out the quartiles based on loan amount")
    st.code(query3)
    st.write(pd.read_sql_query(con=DB,sql=query3).describe())

    st.subheader("Then I divided the data into quartiles, and calculated the % payment percent")
    st.code(query4)

    st.write(pd.read_sql_query(con=DB,sql=query4))
