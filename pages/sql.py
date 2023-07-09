import streamlit as st
import pandas as pd
import gdown
import sqlite3

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
    st.code("""
SELECT
  STRFTIME('%Y-%m-01', DATETIME(loan_timestamp, 'unixepoch')) AS MONTH,
  COUNT(DISTINCT CASE WHEN loan_status = 'declined' THEN LOAN_ID ELSE NULL END) / CAST(COUNT(DISTINCT LOAN_ID) AS FLOAT) AS DECLINED_LOANS_PERC

FROM loans
WHERE STRFTIME('%Y-%m-01', DATETIME(loan_timestamp, 'unixepoch')) = '2019-04-01'
GROUP BY 1
ORDER BY 1 DESC
""")
