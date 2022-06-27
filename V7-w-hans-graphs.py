from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from matplotlib.axis import XAxis, YAxis
import plotly.graph_objs as go
from matplotlib.pyplot import legend

import plotly.express as px
import pandas as pd

external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3',
        'crossorigin': 'anonymous'
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Hans's line graphs setup 
lg = pd.read_csv('line-graph-data.csv')

read_fig = px.line(lg, 
               x='Year', 
               y='readiness_pct_change', 
               line_group='Country', 
               title='Rate of Change in Overall Readiness Index', 
               width=600, 
               height=400,
               color='Country'

               )

vuln_fig = px.line(lg, x='Year', 
                y='vulnerability_pct_change', 
                line_group='Country', 
                title='Rate of Change in Overall Vulnerability Index', 
                width=600, 
                height=400, 
                color='Country')



#Geo Heatmaps Data Setup
geodf = pd.read_csv("https://raw.githubusercontent.com/hxwwong/data101-final-project/main/aseanclimategeo.csv")

#Lyka Bar Charts Data Setup
Vulnerability = pd.read_csv("https://raw.githubusercontent.com/hxwwong/data101-final-project/main/Readiness_Index.csv")
years = Vulnerability['Year'].unique()
countries = Vulnerability['Country'].unique()
country_options = []

for i in countries:
    country_options.append({
        'label': i,
        'value': i
    })

Readiness = pd.read_csv ("https://raw.githubusercontent.com/hxwwong/data101-final-project/main/Readiness_Index.csv")

yearsred = Readiness['Year'].unique()
countries = Readiness['Country'].unique()
country_options = []

for i in countries:
    country_options.append({
        'label': i,
        'value': i
    })

#####Stacked Bar Data
visdf = pd.read_csv("https://raw.githubusercontent.com/hxwwong/data101-final-project/main/visdf.csv")

px.set_mapbox_access_token('pk.eyJ1IjoiYW4tcGFzdHJhbmEiLCJhIjoiY2w0MmNrYXg4MDQ0YTNqcXBhc3hjY2F0YiJ9.8O511QA_q2At57HwfHaVPA')

default_year = 2019

app.layout = html.Div(className = 'container', children = [

    #BG of Information + Hans Things Here---------------------///////////////////
    html.Div(className='row',  children=[
        html.Div(className='col-12', children=[
            html.H1(children=['Signs in the Southeast'], style={"color":"#026440", "font-size":"300%"}),
            html.H2(children=['A Web App for Climate Change Response Assessment in ASEAN'], style={"font-size":"200%"}),

            html.Hr(style={'height': "2px", "width": "100%", "color":"#023020", "opacity":"100%"}),

            html.H4(children = 'Background Information'),
            html.H6(children = ['''
            Climate change poses significant challenges to Southeast Asia. With agriculture accounting for more than 10% of GDP in most countries in this region, the agriculture industry is highly sensitive to the extreme weather events. The continuous rise in climate vulnerability of most countries in this region, as well as the lowering trend of climate readiness bar few exceptions makes a compelling case for action. To facilitate this, we create a dashboard that summarizes high-level essential information in order to present stakeholders with all the necessary tools to make data-driven, high-impact decisions.
            '''], style={"text-align":"justify", "opacity":"80%"}
            )
        ])
    ]),

    # Hans's Line Graphs Here
    html.Div(className='row', children=[
        html.Div(className = 'col-sm-12 col-md-6', children = [
            # html.Img(src=app.get_asset_url('vulnerability.png'), width=600, height=400)
            html.Div(className='col-6', children=[dcc.Graph(figure=read_fig)])
            ]),
        html.Div(className="col-sm-12 col-md-6", children = [
            # html.Img(src=app.get_asset_url('readiness.png'), width=600, height=400)])
            html.Div(className='col-6', children=[dcc.Graph(figure=vuln_fig)])
    ]),

    html.Hr(style={'height': "1px", "width": "100%", "color":"black", "opacity":"100%"}),

    #Boris Geo Maps------------------------------------///////
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            html.H4(children=['Geographical Heatmap'], style={"color":"#026440"}),
            html.H6(children=['Collected by the University of Notre Dame, the Overall Readiness for Climate Change Index is a metric from -1 (least ready) to +1 (most ready), calculated from how prepared various sub-sectors of a country are for climate change. Overall Vulnerability to Climate Change is similarly calculated, with -1 indicating least vulnerable and +1 indicating most vulnerable.'], style={"text-align":"justify", "opacity":"80%"}),
            html.H6(children=['Use this graph by selecting the year on the left side and clicking “Submit.” You may zoom in to better see countries and hover over them to better see their statistics.'], style={"text-align":"justify", "opacity":"80%"})
        ])
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

    #Lyka Grouped Bar Here-----------------------------------------////

    html.Hr(style={'height': "1px", "width": "100%", "color":"black"}),

    #Lyka Bars
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            html.H4(children='Sectoral Vulnerability Indicators in 2019'),
            html.H6(children='insert data description here')
        ])
    ]),

    # Options
    html.Div(className = "row", children=[
        html.Div(className="col-2", children=[
            html.P("Select Country:")
        ]),

        html.Div(className="col-8", children=[
            dcc.Dropdown (id = "select_country",
                multi = False,
                clearable = True,
                disabled = False,
                placeholder = "Select Country of Choice",
                options = country_options, className = "dcc.compon")
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className="col-12", children=[
            dcc.Graph(id="bar-chart1")
        ])
    ]),

    #Lyka Grouped Bar Here 2 #######################################################
    # Options
    html.Hr(style={'height': "1px", "width": "100%", "color":"black"}),

    #Lyka Bars
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            html.H4(children='Sectoral Readiness Indicators in 2019'),
            html.H6(children='insert data description here')
        ])
    ]),

    html.Div(className = "row", children=[
        html.Div(className="col-2", children=[
            html.P("Select Country:")
        ]),

        html.Div(className="col-8", children=[
            dcc.Dropdown (id = "select_country2",
                multi = False,
                clearable = True,
                disabled = False,
                placeholder = "Select Country of Choice",
                options = country_options, className = "dcc.compon")
        ])
    ]),

    html.Div(className="row", children=[
        html.Div(className="col-12", children=[
            dcc.Graph(id="bar-chart2")
        ])
    ]),

    #Vince Bar##################################################################
    html.Hr(style={'height': "1px", "width": "100%", "color":"black"}),

    #Vince
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            html.H4(children='Sources of Total Energy Consumption'),
            html.H6(children='insert data description here')
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-2', children=[
            html.P(['Choose a Country:'])
        ]),

        html.Div(className='col-4', children=[
            dcc.Dropdown(id='dropdownstack',
                options=[{"label":"Brunei Darussalam", "value":"Brunei Darussalam"},
                        {"label":"Cambodia", "value":"Cambodia"},
                        {"label":"Indonesia", "value":"Indonesia"},
                        {"label":"Lao PDR", "value":"Lao PDR"},
                        {"label":"Malaysia", "value":"Malaysia"},
                        {"label":"Myanmar", "value":"Myanmar"},
                        {"label":"Philippines", "value":"Philippines"},
                        {"label":"Singapore", "value":"Singapore"},
                        {"label":"Thailand", "value":"Thailand"},
                        {"label":"Viet Nam", "value":"Viet Nam"}],
                value='Brunei Darussalam')
        ]),


        html.Div(className='col-2', children=[
            html.P(['Choose a year:'])
        ]),
        html.Div(className='col-4', children=[
            html.Div(children=[
                dcc.Slider(1996, 2019, 1, marks=None, id="sliderstack",
                            value=1996,
                            tooltip={"placement": "bottom", "always_visible": True})
            ]),

        ]),
    ]),

   
    html.Div(className='row', children=[
        html.Div(className='col-6', children=[dcc.Graph(id='stack1')]),
        html.Div(className='col-6', children=[dcc.Graph(id='stack2')])
    ]),

    html.Div(className='row', children=[]),
    html.Div(className='row', children=[])
])
]
)

#--------------------------------------------------------------#
#Geo Heatmap1 Callback

@app.callback(
    Output(component_id='the_graph1', component_property='figure'),
    Input(component_id='submit_button', component_property='n_clicks'),
    State(component_id='input_state', component_property='value')
)

def update_output(num_clicks, val_selected):
    #fig = None
    if val_selected is None:
        filter_df = geodf[geodf['Year'] == default_year]
        title = "Overall Vulnerability for " + str(default_year)
    else:
        filter_df = geodf[geodf['Year'] == val_selected]
        title = "Overall Vulnerability for " + str(val_selected)


    fig = px.choropleth(filter_df,
    locations='iso_alpha',
    color="overallvulnerability",
    hover_name="Country",
    hover_data = ["Country", "Year"],
    scope='world',
    title=title,
    center=dict(lat=4.5, lon=115),
    range_color=[-.3, .3],
    color_continuous_scale=px.colors.diverging.RdBu[::-1],
    color_continuous_midpoint = 0)

    fig.update_layout(title=dict(font=dict(size=18),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50),
                          coloraxis_colorbar=dict(
                            title = "Vulnerability Scale",
                            thicknessmode="pixels", thickness=12,
                            lenmode="pixels", len=350,
                            ticks = "inside",
                            tickvals=[-.3, .3],
                            ticktext=['Less Vulnerable', 'More Vulnerable']
                          ))

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(geo_resolution=50)

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
        title = "Overall Readiness for " + str(default_year)
    else:
        filter_df = geodf[geodf['Year'] == val_selected]
        title = "Overall Readiness for " + str(val_selected)

    fig = px.choropleth(filter_df,
    locations='iso_alpha',
    color="overallreadiness",
    hover_name="Country",
    hover_data = ["Country", "Year"],
    scope='world',
    title=title,
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
    fig.update_layout(geo_resolution=50)

    return fig

######### Bar Charts Callback 1 ############3

# Callback to update bar
@app.callback(
    Output('bar-chart1', 'figure'),
    Input('select_country', 'value')
)
def update_bar_by_country(selected_country):
    if selected_country is None:
        graph_df = Vulnerability
    else:
        graph_df = Vulnerability[Vulnerability['Country'] == selected_country]


    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Ecosystem Vulnerability'],
        name='Ecosystem Vulnerability',
        marker_color='#56B4E9'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Exposure'],
        name='Exposure',
        marker_color='#10A67D'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Food Vulnerability'],
        name='Food Vulnerability',
        marker_color='#F0E442'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Habitat Vulnerability'],
        name='Habitat Vulnerability',
        marker_color='#1A89C7'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Health Vulnerability'],
        name='Health Vulnerability',
        marker_color='#D55E00'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Water vulnerability'],
        name='Water Vulnerability',
        marker_color='#95D41D'
    ))

    fig2.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Overall Vulnerability'],
        name='Overall Vulnerability',
        marker_color='#CB0D46'
    ))



    fig2.update_layout(
        title='Vulnerability Score by Sector of Each ASEAN Member States in 2019',
            titlefont_size=25,
        xaxis=dict(
            title='ASEAN Member States',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Vulnerability Score',
            titlefont_size=16,
            tickfont_size=14,
        ))
    fig2.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_title=None)
    return fig2


####Bar Charts Callback 3##########################################
# Callback to update bar
@app.callback(
    Output('bar-chart2', 'figure'),
    Input('select_country2', 'value')
)
def update_bar_by_country(selected_country2):
    if selected_country2 is None:
        graph_df = Readiness
    else:
        graph_df = Readiness[Readiness['Country'] == selected_country2]


    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Overall Readiness'],
        name='Overall Readiness',
        marker_color='#a6cee3'
    ))

    fig.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Social Readiness'],
        name='Social Readiness',
        marker_color='#1f78b4'
    ))

    fig.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Economic Readiness'],
        name='Economic Readiness',
        marker_color='#b2df8a'
    ))

    fig.add_trace(go.Bar(
        x=graph_df['Country'],
        y=graph_df['Government Readiness'],
        name='Government Readiness',
        marker_color='#33a02c'
    ))

    fig.update_layout(
        title='Readiness Score by Sector of Each ASEAN Member States in 2019',
            titlefont_size=25,
        xaxis=dict(
            title='ASEAN Member States',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Readiness Score',
            titlefont_size=16,
            tickfont_size=14,
        ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_title=None)
    return fig

#################

@app.callback(
    Output('stack1', 'figure'),
    [Input(component_id='dropdownstack', component_property='value')]
)
def select_graph(value):
    dff = visdf.copy()
    dff = dff[dff["Country"] == value]

    fig = px.bar(dff, x="Year", y=['Renewable','Non-Renewable'], color='variable', color_discrete_sequence=[px.colors.qualitative.D3[2],px.colors.qualitative.D3[1]], range_y=[0,1])
    fig.update_layout(title="Energy Consumption by source, by Country", font=dict(size=10), title_x=0.15,  yaxis_title="Percentage of Total Energy Consumption")
    #fig.update_layout(width=700, height=500)

    return fig

####stackedbar
@app.callback(
    Output('stack2', 'figure'),
    [Input(component_id='sliderstack', component_property='value')]
)
def select_graph(value):
    dff = visdf.copy()
    dff = dff[dff["Year"] == value]

    fig = px.bar(dff, x="Country", y=['Renewable','Non-Renewable'], color='variable', color_discrete_sequence=[px.colors.qualitative.D3[2],px.colors.qualitative.D3[1]], range_y=[0,1])
    fig.update_layout(title="Energy Consumption by Source, for all ASEAN Nations by Year", font=dict(size=10), title_x=0.15, yaxis_title="Percentage of Total Energy Consumption", xaxis_title=None)
    #fig.update_layout(width=700, height=500)


    return fig

#--------------------------------------------------------------#
if __name__ == '__main__':
    app.run_server(debug=True)
