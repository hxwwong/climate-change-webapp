from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import base64
import os

external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3',
        'crossorigin': 'anonymous'
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

#Read the Data
geodf = pd.read_csv("https://raw.githubusercontent.com/hxwwong/data101-final-project/main/aseanclimategeo.csv")

px.set_mapbox_access_token('pk.eyJ1IjoiYW4tcGFzdHJhbmEiLCJhIjoiY2w0MmNrYXg4MDQ0YTNqcXBhc3hjY2F0YiJ9.8O511QA_q2At57HwfHaVPA')

default_year = 2019

# loading the svg files for the Intro part 
img1 = 'readiness.png'
img2 = 'vulnerability.png'





app.layout = html.Div(className = 'container', children = [
    
    #BG of Information + Hans Things Here
    html.Div(className='row', children=[
        html.H1(children='Signs in the Southeast'),
        html.H2(children='A Web App for D103'),

        html.Hr(),

        html.H4(children = 'Background Information'),
        html.H6(children = '''
        Climate change poses significant challenges to Southeast Asia. With agriculture accounting for more than 10% of GDP in most countries in this region, the agriculture industry is highly sensitive to the extreme weather events. The continuous rise in climate vulnerability of most countries in this region, as well as the lowering trend of climate readiness bar few exceptions makes a compelling case for action. To facilitate this, we create a dashboard that summarizes high-level essential information in order to present stakeholders with all the necessary tools to make data-driven, high-impact decisions.
        '''
        ),

        html.Div(className = 'col-sm', children = [
            html.Img(src=app.get_asset_url('readiness.png'), width=600, height=400)
            ]),
        html.Div(className="col-sm", children = [
            html.Img(src=app.get_asset_url('vulnerability.png'), width=600, height=400)])
    ]),

    html.Hr(),

    #Boris Geo Map 1
    html.Div(className='row', children=[
        html.H3(children='Geographical Heatmap')
    ]),
    
    html.Div(className='row', children=[
        html.Div(className='col-sm', children=[
            dcc.Input(id='input_state', type='number', inputMode='numeric', value=default_year, max=2019, min=1996, step=1, required=True),
            html.Button(id='submit_button', n_clicks=0, children='Submit'),
            html.Div(id='output_state')],
            style={'text_align':'center'}
        ),

    ]), 
    
    html.Div(className='row', children=[
        html.Div(className='col-6', children=[dcc.Graph(id='the_graph1')]),

        html.Div(className='col-6', children=[dcc.Graph(id='the_graph2')])

    ]),

    

    
    
    #Boris Geo Map 2    
    

    html.Div(className='row', children=[]),
    #Lyka Grouped Bar Here
    html.Div(className='row', children=[]),

    #Vince Stacked Bar Here
    html.Div(className='row', children=[]),

    #Extra Divs just in case
    html.Div(className='row', children=[]),
    html.Div(className='row', children=[])
])

#--------------------------------------------------------------#
#Geo Heatmap1
#Only Output needs two 


@app.callback(
    Output(component_id='the_graph1', component_property='figure'),
    Input(component_id='submit_button', component_property='n_clicks'),
    State(component_id='input_state', component_property='value')
)

def update_output(num_clicks, val_selected):
    #fig = None
    if val_selected is None:
        filter_df = geodf[geodf['Year'] == default_year]
    else:
        filter_df = geodf[geodf['Year'] == val_selected]    

    
    fig = px.choropleth(filter_df, 
    locations='iso_alpha',  
    color="overallvulnerability",  
    hover_name="Country", 
    hover_data = ["Country", "Year"],
    scope='asia', 
    title='Overall Vulnerability by Year, 1996 to 2019',  
    center=dict(lat=4.5, lon=115),
    range_color=[-1, 1],
    color_continuous_scale=px.colors.diverging.RdBu[::-1],
    color_continuous_midpoint = 0)

    fig.update_layout(title=dict(font=dict(size=18),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50),
                          coloraxis_colorbar=dict(
                            title = "Vulnerability Scale",
                            thicknessmode="pixels", thickness=12,
                            lenmode="pixels", len=350,
                            ticks = "inside",
                            tickvals=[-1, 1],
                            ticktext=['Least Vulnerable', 'Most Vulnerable']
                          ))
    
    fig.update_geos(fitbounds="locations", visible=False)          

    return fig
    
#------------------------------------------------------------#
#Geo Heatmap 2
@app.callback(
    Output(component_id='the_graph2', component_property='figure'),
    Input(component_id='submit_button', component_property='n_clicks'),
    State(component_id='input_state', component_property='value')
)

def update_output(num_clicks, val_selected):
    if val_selected is None:
        filter_df = geodf[geodf['Year'] == default_year]
    else:
        filter_df = geodf[geodf['Year'] == val_selected]  

    fig = px.choropleth(filter_df, 
    locations='iso_alpha',  
    color="overallreadiness",  
    hover_name="Country",
    hover_data = ["Country", "Year"],
    scope='asia', 
    title='Overall Readiness by Year, 1996 to 2019',  
    center=dict(lat=4.5, lon=115),
    range_color=[-0.1,0.1],
    color_continuous_scale=px.colors.diverging.BrBG,
    color_continuous_midpoint = 0 )

    fig.update_layout(title=dict(font=dict(size=18)),
                          margin=dict(l=60, r=90, t=50, b=50),
                          coloraxis_colorbar=dict(
                            title = "Readiness Scale",
                            thicknessmode="pixels", thickness=12,
                            lenmode="pixels", len=350,
                            ticks = "inside",
                            tickvals=[-0.1, 0.1],
                            ticktext=['Less Ready', 'More Ready']
                          ))
                          
    fig.update_geos(fitbounds="locations", visible=False)                      

    return fig

#--------------------------------------------------------------#
if __name__ == '__main__':
    app.run_server(debug=True)