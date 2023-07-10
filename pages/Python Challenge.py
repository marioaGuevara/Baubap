import plotly.graph_objects as go
import streamlit as st
import gdown
import pandas as pd
import numpy as np
from helpers.auth import check_password
# import matplotlib.pyplot as plt
# import sklearn
# import seaborn as sns
import plotly.express as px

url = 'https://drive.google.com/uc?export=download&id=1Yj53OqHQuAOImizb4q7GEW8NFBfInaky'
output = 'Baubap Python Challenge'
# gdown.download(url, output, quiet=False)
df = pd.read_csv(output)
df.to_csv('data.csv')

st.set_page_config(layout="wide")

if check_password():
    t1, t2, t3 =  st.tabs(["Top Customers", "Support", "Insight 3"])

    with t1:
        st.header("Analysis 1")
        st.subheader("For the first analysis I wanted to take advantage of the demographical data that we have available and focus on understand our most important cohorts.")
        dfTop = df[['genero', 'esEstudiante', 'casado', 'tieneHijos', 'cargosAccumulados', 'CustomerID']]
        dfTop = dfTop.rename(columns={"casado": "Married",
                                        "genero": "Gender",
                                        "esEstudiante": "Is Student",
                                        "tieneHijos": "Has Kids",
                                        "cargosAccumulados": "Cumulative Spent"
                                        }).reset_index()
            
        dfTop = dfTop.groupby(['Gender', 'Is Student', 'Married', 'Has Kids']).agg({'Cumulative Spent':'sum', 'CustomerID': 'count'})
        dfTop['percentOfTotal'] = dfTop['Cumulative Spent'] / sum(dfTop['Cumulative Spent'])
        dfTop['running_total'] = dfTop.sort_values('percentOfTotal', ascending=False)['percentOfTotal'].cumsum()
        dfTop['rank'] = dfTop['running_total'].rank(method='dense', ascending=True)
        dfTop['Include'] = np.where(dfTop['rank'] <= 6, True,False)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(dfTop.sort_values('Cumulative Spent', ascending=False)[['Cumulative Spent', 'Include']],
                        use_container_width=True)
        with col2:        
            fig = px.pie(dfTop[['Include', 'percentOfTotal']], names='Include', values='percentOfTotal')
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Now that we have identified our top customers based on their demographics, we can play close attention to their behaviour.")
        
        dfTop = dfTop.loc[dfTop['rank'] <= 6]
        dfTop.reset_index(inplace=True)
        fig = px.parallel_categories(dfTop[['CustomerID', 'Gender', 'Married', 'Has Kids']],
                                    # dimensions=dfTop[['Gender', 'Is Student', 'Married', 'Has Kids']],
                                    # color=dfTop["CustomerID"]
        )
        st.plotly_chart(fig, use_container_width=True)
        dfTop['Cohort'] = dfTop['Gender'] + " - " + np.where(dfTop["Has Kids"]=="Sí", "Kids", "No Kids") + " - " + np.where(dfTop["Married"]=="Sí", "Married", "Not Married")

        st.dataframe(dfTop.sort_values('rank'))

    with t2:
        def typeOfUser(row):
            if row['usaTabletParaAcceder'] == 0 and row['usaMovilParaAcceder'] == 0:
                return 'Non-mobile user'
            elif row['usaTabletParaAcceder'] == 0 and row['usaMovilParaAcceder'] == 1:
                return 'Mobile User'
            elif row['usaTabletParaAcceder'] == 1 and row['usaMovilParaAcceder'] == 0:
                return 'Tablet User'
            elif row['usaTabletParaAcceder'] == 1 and row['usaMovilParaAcceder'] == 1:
                return 'Tablet + Mobile'
        
        st.header("How's the contact rate by Platform?")
        dfIssiesWithPlatform = df[['haContactoASoporte', 'usaTabletParaAcceder', 'usaMovilParaAcceder', 'CustomerID', 'usuarioPerdido']]
        dfIssiesWithPlatform['haContactoASoporte'] = np.where(dfIssiesWithPlatform['haContactoASoporte'] == 'Sí', 1, 0)
        dfIssiesWithPlatform['usaTabletParaAcceder'] = np.where(dfIssiesWithPlatform['usaTabletParaAcceder'] == 'Sí', 1, 0)
        dfIssiesWithPlatform['usaMovilParaAcceder'] = np.where(dfIssiesWithPlatform['usaMovilParaAcceder'] == 'Sí', 1, 0)
        
        dfIssiesWithPlatform.reset_index(inplace=True)
        dfIssiesWithPlatform['Access Via'] = dfIssiesWithPlatform[['usaTabletParaAcceder', 'usaMovilParaAcceder']].apply(typeOfUser, axis=1)
        
        dfIssiesWithPlatformRaw = dfIssiesWithPlatform
        dfIssiesWithPlatform = dfIssiesWithPlatform.groupby(['Access Via']).agg({'CustomerID': 'count', 'haContactoASoporte': 'sum', 'usuarioPerdido': 'sum'}).reset_index()
        dfIssiesWithPlatform['ContactRate'] = (dfIssiesWithPlatform['haContactoASoporte'].astype(float) / dfIssiesWithPlatform['CustomerID'].astype(float)).apply(lambda x: "{:.2%}".format(x))
        dfIssiesWithPlatform['Churn Rate'] = (dfIssiesWithPlatform['usuarioPerdido'] /  dfIssiesWithPlatform['CustomerID'].astype(float)).apply(lambda x: "{:.2%}".format(x))

        dfIssiesWithPlatform.reset_index()
        dfIssiesWithPlatform = dfIssiesWithPlatform.sort_values('CustomerID', ascending=False)
        

        bar_trace = go.Bar(x=dfIssiesWithPlatform['Access Via'], 
                            y=dfIssiesWithPlatform['CustomerID'], 
                            name='Clients', 
                            text=dfIssiesWithPlatform['CustomerID']
                            )

        line_trace_churn = go.Scatter(x=dfIssiesWithPlatform['Access Via'], 
                                y=dfIssiesWithPlatform['Churn Rate'], 
                                textposition='top center', 
                                mode='lines+markers', 
                                name='Churn Rate', 
                                text=dfIssiesWithPlatform['Churn Rate'],
                                yaxis='y2'
                                )

        line_trace = go.Scatter(x=dfIssiesWithPlatform['Access Via'], 
                                y=dfIssiesWithPlatform['ContactRate'], 
                                textposition='top center', 
                                mode='lines+markers', 
                                name='Contact Rate', 
                                text=dfIssiesWithPlatform['ContactRate'],
                                yaxis='y2'
                                )

        c11, c22 = st.columns(2)
        layout = go.Layout(
                yaxis=dict(title='Customers'),
                yaxis2=dict(title='Contact Rate', overlaying='y', side='right'),
                yaxis3=dict(title='Churn Rate', overlaying='y', side='right'),
                # yaxis3=dict(title='Churn Rate', overlaying='y2', side='right')

            )
        fig = go.Figure(data=[bar_trace,line_trace], layout=layout)
        st.subheader("This could mean that our users are having a hard time with our platform, maybe our app isn't working properly.")
        st.plotly_chart(fig, use_container_width=True)
        
        dfIssiesWithPlatform

        st.subheader("How bad for business is this? Let's examine churn by platform, broken down by the users that have contacted support at some point")
        

        dfIssiesWithPlatformRaw['usuarioPerdido'] = df['usuarioPerdido']
        dfIssiesWithPlatformRaw['haContactoASoporte'] =  np.where(df['haContactoASoporte'] == "Sí", 1, 0)
        dfIssiesWithPlatformRaw['usaTabletParaAcceder'] =  np.where(df['usaTabletParaAcceder'] == "Sí",1,0)

        dfIssiesWithPlatformRaw['usaMovilParaAcceder'] =  np.where(df['usaMovilParaAcceder'] == "Sí",1,0)

        dfIssiesWithPlatformRaw = dfIssiesWithPlatformRaw.groupby(['Access Via', 'haContactoASoporte']).agg({'CustomerID': 'count', 'usuarioPerdido': 'sum'})

        dfIssiesWithPlatformRaw = dfIssiesWithPlatformRaw.reset_index()

        dfIssiesWithPlatformRaw['Churn Rate'] = (dfIssiesWithPlatformRaw['usuarioPerdido'] /  dfIssiesWithPlatformRaw['CustomerID'].astype(float)).apply(lambda x: "{:.2%}".format(x))
        

        churn_w_contact = go.Scatter(x=dfIssiesWithPlatformRaw['Access Via'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 0], 
                                y=dfIssiesWithPlatformRaw['Churn Rate'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 0], 
                                textposition='top center', 
                                mode='lines+markers', 
                                name='Not contacted', 
                                text=dfIssiesWithPlatformRaw['Churn Rate'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 0],
                                yaxis='y'
                                )    
        churn_wo_contact = go.Scatter(x=dfIssiesWithPlatformRaw['Access Via'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 1], 
                                y=dfIssiesWithPlatformRaw['Churn Rate'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 1], 
                                textposition='top center', 
                                mode='lines+markers', 
                                name='Contacted', 
                                text=dfIssiesWithPlatformRaw['Churn Rate'].loc[dfIssiesWithPlatformRaw['haContactoASoporte'] == 1],
                                yaxis='y'
                                )    

        layout = go.Layout(
                yaxis=dict(title='Churn by platform')
                # yaxis3=dict(title='Churn Rate', overlaying='y2', side='right')

            )
        fig = go.Figure(data=[churn_w_contact,churn_wo_contact], layout=layout)
        st.plotly_chart(fig, use_container_width=True)
        st.subheader('As we can see here, people that contacted have a higher retention rate, this can mean 2 things.')
        st.write('1.- Our users need more education on how to use our platform, they need like we are right by their side as they are joining our paltform')
        st.write("2.- We need to improve upon our UI/UX, for some reason some users seem to be getting lost somewhere along the user journey.")
        dfIssiesWithPlatformRaw 

        