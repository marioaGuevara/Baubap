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
    t1, t2, t3 =  st.tabs(["Learners Cohorts", "Support", "Payment Method"])
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
        st.subheader("Our 2 biggest student cohorts are churning disproportionately as compared to other important cohorts (65% vs +77% retention)")
        
        st.header("Explanation:")
        st.write("For the first analysis I wanted to take advantage of the demographical data that we have available and focus on understand our most important cohorts.")
        df['isPrio'] = df.apply(setPriorityCohort, axis=1)
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
        dfTop['Top cohort'] = np.where(dfTop['rank'] <= 6, True,False)
        dfTop['Active'] = dfTop['CustomerID'] - dfTop['usuarioPerdido']
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(dfTop.sort_values('Cumulative Spent', ascending=False)[['Cumulative Spent', 'Top cohort']],
                        use_container_width=True)
        with col2:        
            fig = px.pie(dfTop[['Top cohort', 'percentOfTotal']], names='Top cohort', values='percentOfTotal')
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(dfTop, use_container_width=True)
        st.subheader("Now that we have identified our top customers based on their demographics, we can play close attention to their behaviour.")
        
        dfTopRawOne = df 
        # dfTopRawOne['isPrio'] = df.apply(setPriorityCohort, axis=1)
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
                            text=["Active Learners: " + str(x) for x in dfTopRaw['Active']],
                            yaxis='y'
                            )
        bar_trace_churn = go.Bar(x=dfTopRaw['Cohort'], 
                            y=dfTopRaw['Churn'], 
                            name='Churn', 
                            text=["Churned Learners: " + str(x) for x in dfTopRaw['Active']],
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
        
        st.write("From this view we can understand our current base better, non-students without kids seem to be the majority our our top Learners.")
        
        st.subheader("Let's plot Active Learners, Churned Learners, Retention Rate and the # of Enrolled Courses together.")
        st.plotly_chart(fig, use_container_width=True)
        st.write("From a visual perspectvive, we can sense 2 things. (i) Married people tend to be more engaged as shown by the number of courses they enroll on, and (ii), seems like there's a correlation between said number of courses and retention.")

        st.subheader("We can confirm that last point with a correlation matrix")

        c21, c31 = st.columns(2)
        with c21:
            st.write("A correlation plot confirms that usuarioPerdido (churn) is highly correlated with the number of courses in which a user is enrolled.")
            st.write("As we can see, this means that there's a high correlation between a churned user and  the number of courses in which they enroll, however, it's always important to remember that using a correlation index is not always advisable when using binary series.")
        
        with c31:
            dfCorr=pd.DataFrame()
            dfCorr['Is Churned'] = df['usuarioPerdido']
            dfCorr['Enrolled Courses'] = df['numeroCursosInscritos']
            dfCorr['Married'] = np.where(df['casado'] == 'No', 0,1)
            dfCorr['Has Kids'] = np.where(df['tieneHijos'] == 'No', 0,1)
            dfCorr['Is Student'] = np.where(df['esEstudiante'] == 0, 0,1)
            st.write(dfCorr.corr())
            # dfTopRaw.rename(columns=('numeroCursosInscritos':'nEnrrolledCourses'))
        
        dfEnrolled = df.loc[df['isPrio'] == True][['usuarioPerdido', 'numeroCursosInscritos', 'CustomerID']].groupby('numeroCursosInscritos').agg({'usuarioPerdido': 'sum', 'CustomerID': 'count'}).reset_index()
        dfEnrolled['Enrolled Courses'] = dfEnrolled['numeroCursosInscritos']
        dfEnrolled['Churned'] = dfEnrolled['usuarioPerdido']
        dfEnrolled['Active'] = dfEnrolled['CustomerID'] -  dfEnrolled['usuarioPerdido']
        dfEnrolled['Churn Rate'] = dfEnrolled['usuarioPerdido'] / dfEnrolled['CustomerID']
        dfEnrolled = dfEnrolled.drop(columns=['usuarioPerdido', 'CustomerID', 'numeroCursosInscritos'])
        
        bar_trace_active_enr = go.Bar(x=dfEnrolled['Enrolled Courses'], 
                            y=dfEnrolled['Active'], 
                            name='Active', 
                            text=["Active Learners: " + str(x) for x in dfEnrolled['Active']],
                            yaxis='y'
                            )
        bar_trace_churned = go.Bar(x=dfEnrolled['Enrolled Courses'], 
                            y=dfEnrolled['Churned'], 
                            name='Churned', 
                            text=["Churned: " + str(x) for x in dfEnrolled['Churned']],
                            yaxis='y'
                            )
        line_trace_courses_churn = go.Scatter(    
            x=dfEnrolled['Enrolled Courses'],
            y=dfEnrolled['Churn Rate'],
            textposition='top center',
            mode='lines+markers',
            name='Churn Rate',
            text=dfEnrolled['Churn Rate'].round(2),
            yaxis='y2'
        )
        layout = go.Layout(
                yaxis=dict(title='Customers', showgrid=False), barmode='relative',
                yaxis2=dict(title='', overlaying='y', side='right')
                # , showgrid=False, showdividers=False, showline =False, zeroline=False, showticklabels=False
            )
        fig.update_layout(title=dict(automargin=False), margin=dict(t=0, b=0))
        fig = go.Figure(data=[bar_trace_active_enr, bar_trace_churned, line_trace_courses_churn], layout=layout)

        st.write("Let's double check that and plot the number of courses and Learners based on if they have churned or not.")
        st.plotly_chart(fig, use_container_width=True)

        st.header("Business discussion")
        st.write("Based on the data, it seems safe to conclude that Churn Rate drops dramatically - by 23bps - after a user is enrolled in a second course.")
        st.write("Meanwhile, our 2 biggest student cohorts are churning disproportionately as compared to others similar in size (65% vs +77% retention).")
        st.write("Should we push for Learners to signup for more than one course from the signup? - Based on: the correlation between Churn Rate and Enrolled Courses")
        st.write("Can we target more married customers? - Based on: Better performance overall from married customers")

        st.header("How can we make this better?")
        st.write("This data set is a picture taken at a certain point in time, which limits the understanding we can have on why some some Learners stayed with us longer than others.")
        st.write("""This means that the aforementioned conclusion can be improved upon. \n Maybe some Learners have been with us longer and therefore have not had time to enroll in more courses and spend more money, but might be showing better retention and higher montly payments""",unsafe_allow_html=True)
        

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
        st.subheader("Learners that contacted support are between 33% to 71% less likely to churn.")
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
        st.write("Learners that access our paltform on a mobile device (tablet or phone) disproportionally contact support.")
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
        
        st.header('Business Discussion')
        st.write("Based on these findings, we could conclude that our mobile apps have some areas of opportunity and/or that our Learners need more guidance and support in their leaning journey.")
        st.write('As we scale, a strong Customer Success / Support team might be a factor to consider in our cost structure, on the other hand, we could aim to improve upon our UX/UI which could have an impact on retention.')

        st.header("How can we improve this analysis?")
        st.write("We are missing the reasons why people contacted support and asuming it was due to some issues with our platform.")
    
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    # Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1# Insight 1
    with t3:
        dfRetentionByPlan = df.loc[df['usuarioPerdido']==0]
        st.header("Insight")
        st.subheader("Autopay drives reneue and loyalty.")
        st.header("Analysis")
        dfRetentionByPlan['usaServicioBasicoRegularmente'] = np.where(dfRetentionByPlan['usaServicioBasicoRegularmente'] == 'Sí', 1, 0)
        dfRetentionByPlan['usaServicioPlataRegularmente'] = np.where(dfRetentionByPlan['usaServicioPlataRegularmente'] == 'Sí', 1, 0)
        dfRetentionByPlan['usaServicioOroRegularmente'] = np.where(dfRetentionByPlan['usaServicioOroRegularmente'] == 'Sí', 1, 0)
        dfRetentionByPlan['tipoDeContrato'] = np.where(dfRetentionByPlan['tipoDeContrato'] == 'Mensual', '1 Mensual', np.where(dfRetentionByPlan['tipoDeContrato']=='Trimestral', '2 trimestral', '3 anual'))
        dfRetentionByPlan['haPagadoContenidoIndividual'] = np.where(dfRetentionByPlan['haPagadoContenidoIndividual'] == 'Sí', 1, 0)
        dfRetentionByPlan['haContactoASoporte'] = np.where(dfRetentionByPlan['haContactoASoporte'] == 'Sí', 1, 0)
        dfRetentionByPlan['r6M'] = np.where(dfRetentionByPlan['antiguidad']>=6, 1, 0)
        dfRetentionByPlan['r12M'] = np.where(dfRetentionByPlan['antiguidad']>=12, 1, 0)
        dfRetentionByPlan['r24M'] = np.where(dfRetentionByPlan['antiguidad']>=24, 1, 0)
        dfRetentionByPlan['r36M'] = np.where(dfRetentionByPlan['antiguidad']>=36, 1, 0)
        dfRetentionByPlan['r48M'] = np.where(dfRetentionByPlan['antiguidad']>=48, 1, 0) 
        dfRetentionByPlan['Autopay'] = np.where((dfRetentionByPlan['metodoDePago'] == 'Pago en tienda') | (dfRetentionByPlan['metodoDePago'] == 'Transferencia Bancaria'), 'No', 'Yes')
        dfRetentionByPlan['Gold #'] = np.where(dfRetentionByPlan['tipoDeUsuario']  == 'Oro', 1, 0)
        dfRetentionByPlan['Plata #'] = np.where(dfRetentionByPlan['tipoDeUsuario']  == 'Plata', 1, 0)
        dfRetentionByPlan['Basico #'] = np.where(dfRetentionByPlan['tipoDeUsuario']  == 'Basico', 1, 0)
# 	Tarjeta de credito (Domeciliado		Transferencia Bancaria (Domiciliado)
        by = 'Autopay'
        
        
        dfRetentionByPlan['2P'] = np.where(dfRetentionByPlan['tipoDeContrato']  == '1 Mensual', 1, np.where(dfRetentionByPlan['tipoDeContrato']  == '2 trimestral', 3, 12))
        dfRetentionByPlan['3P'] = np.where(dfRetentionByPlan['tipoDeContrato']  == '1 Mensual', 2, np.where(dfRetentionByPlan['tipoDeContrato']  == '2 trimestral', 6, 24))
        dfRetentionByPlan['4P'] = np.where(dfRetentionByPlan['tipoDeContrato']  == '1 Mensual', 3, np.where(dfRetentionByPlan['tipoDeContrato']  == '2 trimestral', 9, 36))
        dfRetentionByPlan['2p count'] = np.where(dfRetentionByPlan['antiguidad'] > dfRetentionByPlan['2P'], 1,0)
        dfRetentionByPlan['3p count'] = np.where(dfRetentionByPlan['antiguidad'] > dfRetentionByPlan['3P'], 1,0)
        dfRetentionByPlan['4p count'] = np.where(dfRetentionByPlan['antiguidad'] > dfRetentionByPlan['4P'], 1,0)

        dfRetentionByPlan = dfRetentionByPlan[
            [
            by,
            'CustomerID',
            'r6M',
            'r12M',
            'r24M',
            'r36M',
            'r48M',
            'cargosMensuales',
            'antiguidad',
            'haPagadoContenidoIndividual',
            'numeroCursosInscritos',
            'usaServicioBasicoRegularmente',
            'usaServicioPlataRegularmente',
            'usaServicioOroRegularmente',
            'cargosAccumulados',
            '2p count',
            '3p count',
            '4p count',
            'Basico #',
            'Plata #', 
            'Gold #'
            ]
            ].groupby(by).agg({
            'CustomerID': 'count',
            'r6M': 'sum',
            'r12M': 'sum',
            'r24M': 'sum',
            'r36M': 'sum',
            'r48M': 'sum',
            'cargosMensuales': 'mean',
            'antiguidad':'mean',
            'haPagadoContenidoIndividual':'sum',
            'numeroCursosInscritos': 'mean',
            'usaServicioBasicoRegularmente':'sum',
            'usaServicioPlataRegularmente':'sum',
            'usaServicioOroRegularmente':'sum',
            '2p count':'sum',
            '3p count':'sum',
            '4p count':'sum',
            'cargosAccumulados': 'mean',
            'Basico #': 'sum',
            'Plata #': 'sum', 
            'Gold #': 'sum'
            })
        # dfRetentionByPlan['6 Month LTV'] = dfRetentionByPlan['6 Month LTV'] 
        dfRetentionByPlan['Oro %'] = (dfRetentionByPlan['Gold #']  / dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['Plata %'] = (dfRetentionByPlan['Plata #']  / dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['Basico %'] = (dfRetentionByPlan['Basico #']  / dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['Paid for Individual Content'] = (dfRetentionByPlan['haPagadoContenidoIndividual'] / dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['6 M'] =  (dfRetentionByPlan['r6M'] /   dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['12 M'] =  (dfRetentionByPlan['r12M'] /   dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['24 M'] =  (dfRetentionByPlan['r24M'] /   dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['36 M'] =  (dfRetentionByPlan['r36M'] /   dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['48 M'] =  (dfRetentionByPlan['r48M'] /   dfRetentionByPlan['CustomerID']).apply(lambda x: "{:.0%}".format(x))
        dfRetentionByPlan['basicRegularment'] =  dfRetentionByPlan['usaServicioBasicoRegularmente'] /   dfRetentionByPlan['CustomerID']
        dfRetentionByPlan['plataRegularment'] =  dfRetentionByPlan['usaServicioPlataRegularmente'] /   dfRetentionByPlan['CustomerID']
        dfRetentionByPlan['oroRegularmente'] =  dfRetentionByPlan['usaServicioOroRegularmente'] /   dfRetentionByPlan['CustomerID']
        dfRetentionByPlan['LTV'] =  (dfRetentionByPlan['cargosAccumulados']).astype(int).apply(lambda x: "${}".format(x))
        
        # dfRetentionByPlan = dfRetentionByPlan.set_index('metodoDePago')
        dfRetentionByPlan = dfRetentionByPlan.sort_values('6 M', ascending=False)
        
        dfRetentionByPlan = dfRetentionByPlan.reset_index()

        time_series = dfRetentionByPlan[['Autopay', '6 M', '12 M', '24 M', '36 M', '48 M']].melt(id_vars='Autopay', var_name='Time', value_name='Retention %')

        fig = px.line(time_series, x="Time", y="Retention %", color="Autopay", text="Retention %")
        
        c41, c42 = st.columns(2)

        cargo_mensual_si = dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'Yes'].reset_index()['cargosMensuales'][0]
        with c41:
            st.subheader("Autopay")
            st.metric("Monthly Charges", value=f"${cargo_mensual_si.round(2)}")
            
        cargo_mensual_no = dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'No'].reset_index()['cargosMensuales'][0]
        with c42:
            st.subheader("Manual Pay")
            st.metric("Monthly Charges", value=f"${cargo_mensual_no.round(2)}")
            
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("We can set up an experiment in order to drive more business.")
        st.write("Taking into account active clients only, here's how our monthly revenue looks like")

        c61, c62, c63 = st.columns(3)
        with c61:
            discount =st.slider('Select a discount %?', 1, 50, 15)
        
        with c62:
            meses =st.slider('For how many months?', 1, 6, 3)
        
        with c63:
            cambio =st.slider('Change %?', 1, 100, 30)
        
        # dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'Yes'].reset_index()['cargosMensuales'][0]
        months = np.arange(1, 13)
        auto_pay_change = np.concatenate((np.full(meses, cargo_mensual_no*(1-(discount/100))), np.full(12-meses, cargo_mensual_si) ))
        auto_pay_yes = np.full(12, cargo_mensual_si)
        auto_pay_no = np.full(12, cargo_mensual_no)

        users_yes = np.full(12, dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'Yes'].reset_index()['CustomerID'][0])
        users_no = np.full(12, dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'No'].reset_index()['CustomerID'][0]*(1-(cambio/100)))
        users_change = np.full(12, dfRetentionByPlan.loc[dfRetentionByPlan['Autopay'] ==  'No'].reset_index()['CustomerID'][0]*((cambio/100)))
        
        dfExp = pd.DataFrame()
        dfExp['Month'] = months
        dfExp['RR Autopay'] = users_yes * auto_pay_yes
        dfExp['RR Manual pay'] = users_no * auto_pay_no
        dfExp['RR Manual pay Normal'] = (users_no+users_change) * auto_pay_no
        dfExp['RR Converted'] = auto_pay_change * users_change
        dfExp['RR Change'] = dfExp['RR Autopay'] +dfExp['RR Manual pay'] +dfExp['RR Converted']
        dfExp['RR No Change'] = dfExp['RR Autopay'] +dfExp['RR Manual pay Normal']
        
        time_series = dfExp[['Month', 'RR Autopay','RR Manual pay','RR Converted']].melt(id_vars='Month', var_name='Revenue', value_name='Rev')
        time_series_no_change = dfExp[['Month', 'RR Autopay','RR Manual pay Normal']].melt(id_vars='Month', var_name='Revenue', value_name='Rev')
        
        
        time_series = time_series.reset_index()
        time_series_no_change = time_series_no_change.reset_index()
        
        time_series_all = pd.DataFrame()
        time_series_all['Month'] = months
        time_series_all['RR Change'] = dfExp['RR Change']
        time_series_all['RR No Change'] = dfExp['RR No Change']
        time_series_all = time_series_all.melt(id_vars='Month', var_name='Type', value_name='Revenue')
        
        line_yes = go.Scatter(    
            x=time_series_no_change['Month'],
            y=time_series_no_change['Revenue'],
            textposition='top center',
            mode='lines+markers',
            name='Revenue',
            text=time_series_no_change['Revenue'].apply(lambda x: "${}".format(x)),
            hovertemplate=time_series_no_change['Revenue'].apply(lambda x: "${}".format(x)),
            yaxis='y2'
        )

        layout = go.Layout(
                yaxis=dict(title='Customers', showgrid=False), barmode='relative'
            )
        fig.update_layout(title=dict(automargin=False), margin=dict(t=0, b=0))
        fig = go.Figure(data=[line_yes], layout=layout)

        st.plotly_chart(px.bar(time_series_all, x='Month', y='Revenue', color='Type', barmode="group", text=time_series_all['Revenue'].astype(int).apply(lambda x: "{:,.0f}k".format(x/1000))),use_container_width=True)
        c71, c72 = st.columns(2)

        with c71:
            st.plotly_chart(px.bar(time_series, x='Month', y='Rev', color='Revenue', text=time_series['Rev'].astype(int).apply(lambda x: "{:,.0f}k".format(x/1000))))
            
        with c72:
            st.plotly_chart(px.bar(time_series_no_change, x='Month', y='Rev', color='Revenue', text=time_series_no_change['Rev'].astype(int).apply(lambda x: "{:,.0f}k".format(x/1000))))
            