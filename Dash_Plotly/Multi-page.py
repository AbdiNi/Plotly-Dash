import My_dataset as md
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json






# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(__name__, suppress_callback_exceptions=True)



#******** getting figure from dataset  ***************#

# styles = {
#     'pre': {
#         'border': 'thin lightgrey solid',
#         'overflowX': 'scroll'
#     }
# }



#******** generating table  ***************#

def generate_table(dataframe, max_rows=50):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


#********* index ***********#
index_page = html.Div([
    dcc.Link('Visualisation des données ', href='/DataViz'),
    html.Br(),  #saut de ligne
    dcc.Link('Analyse en composante principale', href='/ACP'),
])


#****************************** Page1 *********************************#

page_1_layout = html.Div([
    dcc.Link('Analyse en composante principale', href='/ACP'),
    html.H1('Visualisation des données '),
    html.H2(' 1-Importation des données '),
    generate_table(md.df2016),
    html.Br(),
    html.Br(),
    
#####################################################################
    html.H2(' 2- Présences des pays dans les 50 premières places '),
    dcc.Graph(
        figure=md.fig1
    ),

    html.H2(' 3- Citation et enseignement comparé au classement mondial des 50 meilleures universités en 2016 '),
     dcc.Graph(
        figure=md.fig2
    ),
    html.H2('4- score universitaire pour la recherche en fontion de nombre des étudiants' ),   
     dcc.Graph(
        figure=md.fig3
    ),
    html.H2('5- score universitaire pour la recherche en du classement internationale' ),   
     dcc.Graph(
        figure=md.fig4
    )
############################################################<<<<<<<<<<<
])




#******************************* Page2 *******************************#

page_2_layout = html.Div([
    dcc.Link('Visualisation des données', href='/DataViz'),
    html.H1('Analyse en composante principale'),
   
    html.H2('1- Définiton de l\'ACP '),
    html.P('L\'analyse en composantes principales (ACP ou PCA en anglais pour principal component analysis), ou selon le domaine d\'application la transformation de Karhunen–Loève (KLT)1, est une méthode de la famille de l\'analyse des données et plus généralement de la statistique multivariée, qui consiste à transformer des variables liées entre elles (dites « corrélées » en statistique) en nouvelles variables décorrélées les unes des autres. Ces nouvelles variables sont nommées « composantes principales », ou axes principaux. Elle permet au praticien de réduire le nombre de variables et de rendre l\'information moins redondante.'),
    html.H2('2- Analyse en composantes principales avec PCA de ‘’scikit-learn’’' ),  
    html.H4(' PCA ' ),  
    dcc.Graph(
       figure=md.fig6
    ),

    html.H4(' Valeurs propres' ),  
    dcc.Graph(
       figure=md.fig8
    ),

    html.H4(' Somme des pourcentages des valeurs propres' ),  
    dcc.Graph(
       figure=md.fig7
    ),
    
    html.Div(id='page-2-content'),
    
    
    
])



#**************** Callbacks ***************#
# @app.callback(dash.dependencies.Output('page-1-content', 'children'),
#               [dash.dependencies.Input('page-1-dropdown', 'value')])
# def page_1_dropdown(value):
#     return 'You have selected "{}"'.format(value)


# @app.callback(dash.dependencies.Output('page-2-content', 'children'),
#               [dash.dependencies.Input('page-2-radios', 'value')])
# def page_2_radios(value):
#     return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])



#******************************* Display ******************************#

def display_page(pathname):
    if pathname == '/DataViz':
        return page_1_layout
    elif pathname == '/ACP':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
