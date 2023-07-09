import streamlit as st
import pandas as pd 
from helpers.auth import check_password

st.set_page_config(layout="wide")

if check_password():
    print('Hola')