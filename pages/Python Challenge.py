import streamlit as st
import gdown
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
import plotly.express as px

url = 'https://drive.google.com/uc?export=download&id=1Yj53OqHQuAOImizb4q7GEW8NFBfInaky'
output = 'Baubap Python Challenge'
gdown.download(url, output, quiet=False)
df = pd.read_csv(output)
df.to_csv('data.csv')
print(df.columns)