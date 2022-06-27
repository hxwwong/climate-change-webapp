from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from matplotlib.axis import XAxis, YAxis
import plotly.graph_objs as go
from matplotlib.pyplot import legend

import plotly.express as px
import pandas as pd



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

### calling them into the divs they're supposed to go into 

dcc.Graph(fig=read_fig) 
dcc.Graph(fig=vuln_fig)