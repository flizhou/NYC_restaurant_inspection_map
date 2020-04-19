import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.express as px
from scripts.plot import plot_map, plot_grades_boro, plot_grades_cuisine, plot_restaurants

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server

app.title = 'Restaurant inspection map in New York'

# Load data 
rst_info = pd.read_pickle('data/clean_data/nyc_restaurants_info.pkl')
isp_info = pd.read_pickle('data/clean_data/nyc_restaurants_grades.pkl')
analysis_data = pd.read_pickle('data/clean_data/nyc_restaurants_analysis.pkl').replace('-2', 'NA')

# Load layer dict
with open('data/clean_data/borough_loc.json', 'r') as json_data:
    layer = json.load(json_data)

# Get cuisine list
cuisines = rst_info['cuisine description'].unique()


# Set up the app layout
app.layout = html.Div([

    html.H1("Restaurant inspection map in New York"),
    html.P(
        "Please",
        className='description'
    ),

    html.Iframe(
        sandbox='allow-scripts',
        id='map-plot',
        height='500',
        width='900',
        style={'border-width': '0'},
        srcDoc=plot_map(rst_info, layer).to_html(),
        className='right-col'
    ),

    dcc.Tabs([

        # first tab
        dcc.Tab(label='Borough', children=[

            html.Iframe(
                sandbox='allow-scripts',
                id='plot-1',
                height='500',
                width='800',
                srcDoc=plot_grades_boro(analysis_data).to_html(),
                style={'border-width': '0'},
            ),

            html.P('Choose borough:', className='dropdown'),
            dcc.Dropdown(
                id='boro',
                options=list(
                    {"label": i, "value": i} for i in ['Manhattan', 'Bronx', 'Brooklyn', 
                                                        'Queens', 'Staten Island']),
                value='Manhattan',
                clearable=False
            ),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot-2',
                height='900',
                width='800',
                style={'border-width': '0'},
            ),

        ]),
                
        # second tab
        dcc.Tab(label='Cusine type', children=[

            html.P('Choose cuisine type:', className='dropdown'),
            dcc.Dropdown(
                id='cuisine-type',
                options=list(
                    {"label": i, "value": i} for i in cuisines),
                multi = True,
                value=['American'],
                clearable=False
            ),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot-3',
                height='500',
                width='800',
                style={'border-width': '0'},
            )
        ]),
            
        # third tab
        dcc.Tab(label='Restaurants', children=[

            html.P('Choose restaruants:', className='dropdown'),
            dcc.Dropdown(
                id='restaurants',
                options=list(
                    {"label": i, "value": i} for i in rst_info.camis),
                multi = True,
                value = rst_info.camis[:3],
                clearable=False
            ),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot-4',
                height='500',
                width='800',
                style={'border-width': '0'},
            )
        ])
    ], className='container-2'),


    dcc.Markdown(
        '''

        Data sources: [DOHMH New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/rs6k-p7g6) \
            dataset from [New York City OpenData](https://opendata.cityofnewyork.us/)

        '''
    ),
])


@app.callback(
    dash.dependencies.Output('plot-2', 'srcDoc'),
    [dash.dependencies.Input('boro', 'value')])
def update_plot(boro):
    '''

    '''
    plot_2 = plot_grades_cuisine(analysis_data[analysis_data['boro'] == boro],
                                 'in' + boro).to_html()
    return plot_2

@app.callback(
    dash.dependencies.Output('plot-3', 'srcDoc'),
    [dash.dependencies.Input('cuisine-type', 'value')])
def update_plot(cuisine_type):
    '''

    '''
    plot_3 = plot_grades_cuisine(analysis_data[analysis_data['cuisine description'].isin(cuisine_type)],
                                 '', True).to_html()
    return plot_3

@app.callback(
    dash.dependencies.Output('plot-4', 'srcDoc'),
    [dash.dependencies.Input('restaurants', 'value')])
def update_plot(restaurants):
    '''

    '''
    plot_4 = plot_restaurants(isp_info[isp_info['camis'].isin(restaurants)].copy()).to_html()
    return plot_4

if __name__ == '__main__':

    app.run_server(debug=True)