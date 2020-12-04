import plotly.express as px
import plotly.graph_objs as go
import pandas as pd 
from sklearn.decomposition import PCA
import numpy as np


#****************** Récupération des données CSV ************************#

df = pd.read_csv("https://simplonline-v3-prod.s3.eu-west-3.amazonaws.com/media/file/csv/be67fa74-2c34-419c-9249-050394a7eb3e.csv")
# df2016 = df[df.year == 2016].iloc[:50,:]
# df2016['world_rank'] = df2016['world_rank'].replace(['=39'],'39')
# df2016['world_rank'] = df2016['world_rank'].replace(['=44'],'44')
# df2016['world_rank'] = df2016['world_rank'].replace(['=47'],'47')
# df2016["num_students"]  = [str(each).replace(',', '') for each in df2016["num_students"]]

df2016 = df[df.year == 2016].iloc[:58,:]  # 8lines contains "NaN"
df2016
df2016 = df2016.dropna()
df2016.isnull().sum()
print(len(df2016))
df2016

def convertGender (x):
    a, b= x.split(':')
    c = format(int(a)/int(b), ".2f")
    return c

df2016['female_male_ratio'] = df2016['female_male_ratio'].apply(convertGender)

df2016.world_rank = [int(each.replace('=','')) for each in df2016.world_rank]
df2016['international_students'] = df2016['international_students'].str.replace(r'%', r'.0').astype('float') / 100.0
df2016['num_students'] = df2016['num_students'].str.replace(r',', r'.').astype('float') 
df2016['income'] = df2016['income'].astype('float') 
df2016['international'] = df2016['international'].astype('float') 
df2016['total_score'] = df2016['total_score'].astype('float') 

df_2016 = df2016.drop(['year', 'university_name','country'], axis=1)

#nombre d'observations
n = df_2016.shape[0]
#nombre de variables
p = df_2016.shape[1]

# figure1
fig1 = px.scatter(df2016, x="country", y="world_rank", color="country")
fig1.update_layout(clickmode='event+select')
fig1.update_traces(marker_size=20)

# figure2 
trace1 = go.Scatter( x = df2016.world_rank,y = df2016.citations,
                    mode = "lines", name = "citations",marker = dict(color = 'rgba(16, 112, 2, 0.8)'),text = df.university_name)
trace2 = go.Scatter( x = df2016.world_rank,y = df2016.teaching,
                    mode = "lines+markers",name = "enseignement",marker = dict(color = 'rgba(80, 26, 80, 0.8)'),text = df.university_name)
data = [trace1, trace2]
layout = dict(title = 'Citation et enseignement comparé au classement mondial des 50 meilleures universités en 2016',
              xaxis = dict(title = 'Rang Mondial',ticklen = 5,zeroline= False))
fig2 = dict(data = data, layout = layout)


# figure3

fig3 = px.scatter(df2016, x="num_students", y="citations",color="country")
fig3.update_layout(clickmode='event+select')
fig3.update_traces(marker_size=20)


# figure3

fig4 = px.scatter(df2016, x="world_rank", y="citations",color="country")
fig4.update_layout(clickmode='event+select')
fig4.update_traces(marker_size=20)



############### Figures pour page 2 ######################
# PCA 

#1- FIRST-FIG
df_2016 = df2016.drop(['year', 'university_name','country'], axis=1)
#features = ["sepal_width", "sepal_length", "petal_width", "petal_length"]
features =  ['world_rank','teaching','research','citations',]
fig5 = px.scatter_matrix(
    df_2016,
    dimensions=features,
    #color="species"
)
fig5.update_traces(diagonal_visible=False)


# 2- ACP-FIG
pca = PCA(n_components=4)
components = pca.fit_transform(df_2016)
labels = {
    str(i): f"PC {i+1} ({var:.1f}%)"
    for i, var in enumerate(pca.explained_variance_ratio_ * 100)
}

fig6 = px.scatter_matrix(
    components,
    labels=labels,
    dimensions=range(4),
    
)
fig6.update_traces(diagonal_visible=False)



# 3- cumsum pca.explained variance

pca2 = PCA()
pca2.fit(df_2016)
val_prop = ((n-1)/n*pca2.explained_variance_)/100
exp_var_cumul = np.cumsum(pca2.explained_variance_ratio_)

fig7 = px.area(
    x=range(1, exp_var_cumul.shape[0] + 1),
    y=exp_var_cumul,
    labels={"x": "# Components", "y": "cumul_variance"}
)

fig8 = px.area(
    x=range(1, val_prop.shape[0] + 1),
    y=val_prop,
    labels={"x": "# Components", "y": "variance"}
)



