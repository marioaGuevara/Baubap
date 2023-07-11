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
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    with t1:
        def setPriorityCohort(row):
            if (row['genero'] == 'Masculino' and row['esEstudiante'] == 0 and row['casado'] == "Sí") or (row['genero'] == 'Masculino' and row['esEstudiante'] == 0 and row['casado'] == "No" and row['tieneHijos'] == "No"):
                return True
            if (row['genero'] == 'Feminino' and row['esEstudiante'] == 0 and row['casado'] == "Sí") or (row['genero'] == 'Feminino' and row['esEstudiante'] == 0 and row['casado'] == "No" and row['tieneHijos'] == "No"):
                return True
            return False
            
        st.header("Insight:")
        st.subheader("Our 2 biggest student cohorts are churning disproportionately, we can prevent that by pushing for more enrollment in courses.")
        
        st.header("Explanation:")
        st.write("For the first analysis I wanted to take advantage of the demographical data that we have available and focus on understand our most important cohorts.")

        dfTop = df[['genero', 'esEstudiante', 'casado', 'tieneHijos', 'cargosAccumulados', 'CustomerID', 'usuarioPerdido','cargosMensuales','antiguidad', 'numeroCursosInscritos']]

        dfTop = dfTop.rename(columns={"casado": "Married",
                                        "genero": "Gender",
                                        "esEstudiante": "Is Student",
                                        "tieneHijos": "Has Kids",
                                        "cargosAccumulados": "Cumulative Spent"
                                        }).reset_index()
            
        dfTop = dfTop.groupby(['Gender', 'Is Student', 'Married', 'Has Kids']).agg({'Cumulative Spent':'sum', 'CustomerID': 'count', 'usuarioPerdido': 'sum',    'cargosMensuales': 'mean', 'antiguidad': 'mean', 'numeroCursosInscritos': 'mean'})
        dfTop['percentOfTotal'] = dfTop['CustomerID'] / sum(dfTop['CustomerID'])
        dfTop['Retention Rate'] = 1 - (dfTop['usuarioPerdido'] / dfTop['CustomerID'])
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
        
        dfTopRawOne = df 
        dfTopRawOne['isPrio'] = df.apply(setPriorityCohort, axis=1)
        dfTopRaw = dfTopRawOne

        fig = px.parallel_categories(dfTopRaw.loc[dfTopRaw['isPrio'] == True],
                                    dimensions=dfTopRaw.loc[dfTopRaw['isPrio'] == True][['genero', 'esEstudiante', 'casado', 'tieneHijos']],
        )
        fig.update_layout(margin=dict(b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        dfTopRaw = dfTopRaw.loc[dfTopRaw['isPrio'] == True]
        dfTopRaw['KidsCohort'] = np.where(dfTopRaw['tieneHijos'] == "No", " - No-kids", " - Kids")
        dfTopRaw['MarriedCohort']=  np.where(dfTopRaw['casado'] == "No", " - Unmarried", " - Married")
        dfTopRaw["GenderCohort"] = np.where(dfTopRaw['genero'] == 'Feminino', 'Female', 'Male')
        dfTopRaw['Cohort'] = np.where(dfTopRaw['isPrio'] == True, dfTopRaw["GenderCohort"] + dfTopRaw['KidsCohort'] + dfTopRaw['MarriedCohort'], "Else")
        

        dfTopRaw = dfTopRaw[['Cohort', 'usuarioPerdido','CustomerID', 'numeroCursosInscritos']].groupby(['Cohort']).agg({'CustomerID': 'count', 'usuarioPerdido': 'sum', 'numeroCursosInscritos': 'mean'}).reset_index()
        dfTopRaw['Churn Rate'] = dfTopRaw['usuarioPerdido']/ dfTopRaw['CustomerID']
        dfTopRaw['Retention Rate'] = 1 - dfTopRaw['Churn Rate']
        dfTopRaw['Churn'] = dfTopRaw['usuarioPerdido']
        dfTopRaw['Active'] =  dfTopRaw['CustomerID'] - dfTopRaw['usuarioPerdido']
        x = dfTopRaw['Cohort']
        
        dfTopRaw = dfTopRaw.sort_values('Active', ascending=False)

        bar_trace_active = go.Bar(x=dfTopRaw['Cohort'], 
                            y=dfTopRaw['Active'], 
                            name='Active', 
                            text=["Active Users: " + str(x) for x in dfTopRaw['Active']],
                            yaxis='y'
                            )
        bar_trace_churn = go.Bar(x=dfTopRaw['Cohort'], 
                            y=dfTopRaw['Churn'], 
                            name='Churn', 
                            text=["Churned Users: " + str(x) for x in dfTopRaw['Active']],
                            yaxis='y'
                            )

        line_trace = go.Scatter(    
            x=dfTopRaw['Cohort'],
            y=dfTopRaw['Retention Rate'],
            textposition='top center',
            mode='lines+markers',
            name='Retention Rate',
            text=dfTopRaw['Retention Rate'].apply(lambda x: "{:.2%}".format(x)),
            hovertemplate=dfTopRaw['Retention Rate'].apply(lambda x: "{:.2%}".format(x)),
            yaxis='y2'
        )

        line_trace_courses = go.Scatter(    
            x=dfTopRaw['Cohort'],
            y=dfTopRaw['numeroCursosInscritos'],
            textposition='top center',
            mode='lines+markers',
            name='Enrolled Courses',
            text=dfTopRaw['numeroCursosInscritos'].round(2),
            yaxis='y3'
        )

        c11, c22 = st.columns(2)

        layout = go.Layout(
                yaxis=dict(title='Customers', showgrid=False), barmode='relative',
                yaxis2=dict(title='', overlaying='y', side='right', range=[0, 1], showgrid=False, showdividers=False, showline =False, zeroline=False, showticklabels=False),
                yaxis3=dict(title='', overlaying='y', side='right',range=[0, 10], showgrid=False, showdividers=False, showline =False, zeroline=False, showticklabels=False),
            )
        fig.update_layout(title=dict(automargin=False), margin=dict(t=0, b=0))
        fig = go.Figure(data=[bar_trace_active, bar_trace_churn,line_trace, line_trace_courses], layout=layout)
        
        st.write("From this view we can understand our current base better, non-students without kids seem to be the majority our our top users.")
        
        st.subheader("Let's plot Active Users, Churned Users, Retention Rate and the # of Enrolled Courses together.")
        st.plotly_chart(fig, use_container_width=True)
        st.write("From a visual perspectvive, we can sense 2 things. (i) Married people tend to be more engaged as shown by the number of courses they enroll on, and (ii), seems like there's a correlation between said number of courses and retention.")

        st.subheader("We can confirm that last point with a correlation matrix")

        c21, c31 = st.columns(2)
        with c21:
            st.write("A correlation plot confirms that usuarioPerdido (churn) is highly correlated with the number of courses in which a user is enrolled.")
            st.write("As we can see, this means that there's a high correlation between a churned user and  the number of courses in which they enroll.")
        
        with c31:
            dfCorr=pd.DataFrame()
            dfCorr['Is Churned'] = df['usuarioPerdido']
            dfCorr['Enrolled Courses'] = df['numeroCursosInscritos']
            dfCorr['Married'] = np.where(df['casado'] == 'No', 0,1)
            dfCorr['Has Kids'] = np.where(df['tieneHijos'] == 'No', 0,1)
            dfCorr['Is Student'] = np.where(df['esEstudiante'] == 0, 0,1)
            st.write(dfCorr.corr())
            # dfTopRaw.rename(columns=('numeroCursosInscritos':'nEnrrolledCourses'))
        
        st.header("Conclusion")
        st.write("Based on the number of courses users enroll on - our top users are churning because they don't see the value in our platform, however, once we can prove our worth, they tend to stay with us at a higher rate than those with poor engagement (< 4 courses)")
        
        
        
    
        


    #Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2
    #Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2
    #Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2#Insight 2
    # I2 
    with t2:
        def typeOfUser(row):
            if row['usaTabletParaAcceder'] == 0 and row['usaMovilParaAcceder'] == 0:
                return '1 Non-mobile user'
            elif row['usaTabletParaAcceder'] == 0 and row['usaMovilParaAcceder'] == 1:
                return '2 Mobile User'
            elif row['usaTabletParaAcceder'] == 1 and row['usaMovilParaAcceder'] == 0:
                return '3 Tablet User'
            elif row['usaTabletParaAcceder'] == 1 and row['usaMovilParaAcceder'] == 1:
                return '4 Tablet + Mobile'
        
        st.header("Insight")
        st.subheader("Users that contacted support are between 33% to 71% less likely to churn.")
        st.header("Explanation")
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
        st.write("Users that access our paltform on a mobile device (tablet or phone) disproportionally contact support.")
        st.plotly_chart(fig, use_container_width=True)
        
        dfIssiesWithPlatform
        st.write(" ")
        st.write("Let's examine this from a churn rate perspective.")
        

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
        
        dfIssiesWithPlatformRaw 
        
        st.header('Conclusion')
        st.write('1.- As we scale, a strong Customer Success / Support team might be a factor to consider in our cost structure, user might need more guidance than we are anticipating or...')
        st.write("2.- We need to improve upon our UI/UX.")



        