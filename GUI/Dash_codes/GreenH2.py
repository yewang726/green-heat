# -*- coding: utf-8 -*-
"""
@author: Ahmad Mojiri
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import os
from assets.component_model import SolarResource, WindSource
from assets.optimisation import Optimise
from assets.plotting import prep_results_to_print

colors = {'background': 'whitesmoke',
          'text': 'black'}
folder = (r'\\piso.cecs.anu.edu.au\fealab\SodiumLabData')
#folder = (r'C:\Users\z3337922\Downloads\sodium_lab_data')

locations = [{'label':'Newman','value':'Newman'},
             {'label':'Tom Price','value':'Tom_Price'},
             {'label':'Whyalla','value':'Whyalla'},
             {'label':'Gladstone','value':'Gladstone'},
             {'label':'Pinjara','value':'Pinjara'},
             {'label':'Port Agusta','value':'Port_Augusta'},
             {'label':'Burnie','value':'Burnie'},]

storage_types = [{'label':'Salt Cavern','value':'Salt Cavern'},
                 {'label':'Lined Rock Cavern','value':'Lined Rock'}]

Layout= {'xaxis':{'showline':True, 'linewidth':1.25,
                  'mirror':True,'linecolor':'black',
                  'nticks':20, 'tickangle':30,
                  'gridcolor':'LightPink'},
         'yaxis':{'showline':True, 'linewidth':1.25,
                  'mirror':True,'gridcolor':'LightPink'},
         'legend':{'yanchor':"bottom", 'y':1,
                   'xanchor':"left",'x':0.1,'orientation':'h'},
                   'plot_bgcolor': colors['background'],
           'title':'',
           'font': {'color': colors['text']}  }


app = dash.Dash(__name__)

app.layout = html.Div([
            dbc.Row(dbc.Col(html.H1('Green H2'),
                            width={'size':6, 'offset':5}
                      )),
            
            dbc.Row(dbc.Col(html.H2('Solar Thermal Group - Australian National University'),
                            width={'size':7, 'offset':3}
                      )),
            
            
            dbc.Row([
                     dbc.Col(children= html.Div('Electrolyser efficiency:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     
                     dbc.Col(dcc.Input(id="EL_ETA", type="number",
                                       value=0.7,
                                       min=0.5,
                                       max=1.0,
                                       step=0.1,
                                       style={}),
                             width={'size':1, 'offset':0}
                             ),
                     
                     
                     
 #Location                     
                     dbc.Col(dcc.Loading(
                                id="Lolcation_Status",
                                type="default",
                                children= html.Div('None has been selected!',
                                                   id='location_status',
                                                   style={'textAlign': 'right'})),
                             width={'size':2, 'offset':1}
                             ),
                     
                     dbc.Col(dcc.Dropdown( id='location_selector',
                                          options=locations,
                                          multi=False,
                                          searchable=True,
                                          placeholder='Select a location!'
                                    ),width={'size':2, 'offset':0}
                                 ),
                    
                     ]),

   
            
#Battery charging efficiency            
            dbc.Row([dbc.Col(children= html.Div('Battery charging efficiency:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     
                     dbc.Col(dcc.Input(id="BAT_ETA_IN", type="number",
                                       value=0.95,
                                       min=0.1, max=1.0,
                                       step=0.05, style={}),
                             width={'size':1, 'offset':0}
                             ),
 #Storage type             
            dbc.Col(children= html.Div('UG Storage type:',
                                       style={'textAlign': 'right'}),
                width={'size':2, 'offset':1}
                ),
                     
            dbc.Col(dcc.Dropdown( id='storage_selector',
                                 options=storage_types,
                                 multi=False,
                                 searchable=True,
                                 placeholder='Select UG storage'
                           ),width={'size':2, 'offset':0}
                        ),
                     ]),



                     
   
            
#Battery discharging efficiency            
            dbc.Row([
                    dbc.Col(children= html.Div('Battery discharging efficiency:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                    
                     dbc.Col(dcc.Input(id="BAT_ETA_OUT", type="number",
                                       min=0.1, max=1.0,
                                       value=0.95,
                                       step=0.05, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     
                     
                     ]),

            
#Cost of PV            
            dbc.Row([
                    dbc.Col(children= html.Div('Unit cost of PV:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_PV", type="number",
                                       min=0.0,
                                       value=1122,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kW',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            
            
#Cost of Wind            
            dbc.Row([
                    dbc.Col(children= html.Div('Unit cost of Wind:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_WIND", type="number",
                                       min=0.0,
                                       value=1455,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kW',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),


            
#Cost of Electrolyser            
            dbc.Row([
                    dbc.Col(children= html.Div('Unit cost of Electrolyser:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_EL", type="number",
                                       min=0.0,
                                       value=1067,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kW',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            
#UG_STORAGE_CAPA_MAX            
            dbc.Row([
                    dbc.Col(children= html.Div('UG storage max capacity:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="UG_STORAGE_CAPA_MAX", type="number",
                                       min=0.0,
                                       value=1e8,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('kg of H2',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            
            
#C_PIPE_STORAGE            
            dbc.Row([
                    dbc.Col(children= html.Div('Unit cost of pipe storage:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_PIPE_STORAGE", type="number",
                                       min=0.0,
                                       value=516,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kg of H2',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            
            
#PIPE_STORAGE_CAPA_MIN            
            dbc.Row([
                    dbc.Col(children= html.Div('Pipe storage min capacity:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="PIPE_STORAGE_CAPA_MIN", type="number",
                                       min=0.0,
                                       value=1e5,
                                       step=1000, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('kg of H2',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            
   
            
#C_BAT_ENERGY            
            dbc.Row([
                    dbc.Col(children= html.Div('Battery energy unit price:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_BAT_ENERGY", type="number",
                                       min=0.0,
                                       value=196,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kWh',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1})
                     ]),
            

#C_BAT_POWER            
            dbc.Row([
                    dbc.Col(children= html.Div('Battery power unit price:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="C_BAT_POWER", type="number",
                                       min=0,
                                       value=405,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('USD/kW',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1}
                             ),
                     ]),
            
#CF            
            dbc.Row([
                    dbc.Col(children= html.Div('Capcaity factor:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="CF", type="number",
                                       min=1, max=100,
                                       value=100,
                                       step=1, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('Percent[%]',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1}
                             ),
                     ]),
            
#Load            
            dbc.Row([
                    dbc.Col(children= html.Div('Load:',
                                                style={'textAlign': 'right'}),
                             width={'size':2, 'offset':0}
                             ),
                     dbc.Col(dcc.Input(id="LOAD", type="number",
                                       min=0.0,
                                       value=5.0,
                                       step=0.05, style={}),
                             width={'size':1, 'offset':0}
                             ),
                     dbc.Col(children= html.Div('kgH2/s',
                                                style={'textAlign': 'left'}),
                             width={'size':1, 'offset':1}
                             ),
                     ]),


            
            dbc.Row([dbc.Col(html.Button('Optimise!',
                                         id='Optimise',
                                         n_clicks=0),
                                width={'size':1, 'offset':1}
                                   ),
 #print results
                    
                     dbc.Col(dcc.Loading(
                                    id="OPTIMISATION_TEXT",
                                    type="default",
                                    children= html.Div('Progress!',
                                                       id='optimisation_text')),
                                 width={'size':1, 'offset':0}
                                 ),
            
            dbc.Col(dcc.Textarea(id='Output',
                                 value='',
                                 readOnly=True,
                                 style={'width':'100%','height':200}
                                 ),
                                 width={'size':3, 'offset':2}
                    
                    ),
            
                     ]),  
             
            
            dbc.Row(dbc.Col(dcc.Graph(id='GraphI',figure={'data':[]}),
                            width={'size':10, 'offset':1}
                        )),
            
            
            
            ])


              

#-------------------------------------
@app.callback(
            [Output('OPTIMISATION_TEXT','children'),
             Output('Output', 'value')],
            [Input('Optimise','n_clicks'),
             State('EL_ETA', 'value'),
             State('BAT_ETA_IN', 'value'),
             State('BAT_ETA_OUT', 'value'),
             State('C_PV', 'value'),
             State('C_WIND', 'value'),
             State('C_EL', 'value'),
             State('UG_STORAGE_CAPA_MAX', 'value'),
             State('C_PIPE_STORAGE', 'value'),
             State('PIPE_STORAGE_CAPA_MIN', 'value'),
             State('C_BAT_ENERGY', 'value'),
             State('C_BAT_POWER', 'value'),
             State('LOAD', 'value'),
             State('CF', 'value'),
             State('location_selector','value'),
             State('storage_selector','value')],
             prevent_initial_call=True
            )
def optimise(click, el_eta, bat_eta_in, bat_eta_out, c_pv, c_wind, c_el,
             ug_storage_capa_max, c_pipe_stprage, pipe_storage_capa_min,
             c_bat_energy, c_bat_power, load, cf, location, storage_type):
      try:
          SolarResource(location)
      except:
          text = 'Error: Choose a location!'
          results_to_print = 'None'
      else:
          SolarResource(location)
          WindSource(location)
          simparams = dict(EL_ETA = el_eta,       
                           BAT_ETA_in = bat_eta_in, 
                           BAT_ETA_out = bat_eta_out,  
                           C_PV = c_pv,          
                           C_WIND = c_wind,        
                           C_EL = c_el,          
                           UG_STORAGE_CAPA_MAX = ug_storage_capa_max, 
                           C_PIPE_STORAGE = c_pipe_stprage,
                           PIPE_STORAGE_CAPA_MIN = pipe_storage_capa_min, 
                           C_BAT_ENERGY = c_bat_energy,        
                           C_BAT_POWER = c_bat_power,        
                             ) 
          text = 'Completed!'
          results = Optimise(load, cf, storage_type, simparams)
          results_to_print = prep_results_to_print(results,simparams)
          
      return ([text,results_to_print])





@app.callback(
            [Output('location_status','children')],
            [Input('location_selector','value')],
            prevent_initial_call=True
             )
def update_weather_data(location):
    try:
        SolarResource(location)
    except:
        text = '%s has been selected'%(location)
    else:
        SolarResource(location)
        WindSource(location)
        text = 'Weather data updated!'
    return([text])
            
            


if __name__ == '__main__':
    app.run_server(debug=True)
