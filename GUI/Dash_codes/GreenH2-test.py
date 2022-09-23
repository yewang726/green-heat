# -*- coding: utf-8 -*-
"""
@author: Ahmad Mojiri
"""

import dash
from dash import html
import dash_bootstrap_components as dbc


colors = {'background': 'whitesmoke',
          'text': 'black'}



app = dash.Dash(__name__)

app.layout = html.Div([
            dbc.Row(dbc.Col(html.H1('Green H2'),
                            width={'size':6, 'offset':5}
                      )),
            
            dbc.Row(dbc.Col(html.H2('Solar Thermal Group - Australian National University'),
                            width={'size':7, 'offset':3}
                      )),
            ])
            
            
            
          


if __name__ == '__main__':
    app.run_server(debug=False)
