
import pandas as pd
import numpy as np
import plotly.express as px


def plot_map(data, layer):
    """
    Returns a map graph of all restaurants.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample.  
    layer: dict
        the borough location

    Returns:
    --------
    plotly figure
        a map graph of all restaurants
    """

    token = 'pk.eyJ1IjoiZmxpemhvdSIsImEiOiJjazg4Y2hjaW4wMjFlM3NtemhhNG90Z2ZzIn0.gxDbD64mpZbxE2HMjxEZng'
    #token = TOKEN

    fig = px.scatter_mapbox(data, lat='latitude', lon='longitude', 
                            hover_name='dba', 
                            hover_data=['boro', 'current_grade', 'cuisine description',
                                        'building', 'street', 'zipcode', 'phone'],
                            color='boro',
                            center=dict(lat=40.7, lon=-73.97), 
                            zoom=9.5, 
                            height=550,
                            width=800)

    fig.update_layout(mapbox_accesstoken=token,
                      mapbox_layers=layer,
                      margin={"r":0,"t":0,"l":0,"b":0},
                      legend_title='Borough',
                      clickmode="event+select",
                      dragmode="lasso")
    
    return fig
    
def get_selected_dba(selection):
    """

    """
    ind = []
    for point in selection['points']:
        ind.append(point['hovername'])
    return ind

def plot_grades_boro(data):
    """
    Returns a bar graph of grades based on borough.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample.  
        
    Returns:
    --------
    plotly figure
        a bar graph of grades based on borough
    """
    df = data.groupby(['boro', 'grade'])[['count']].sum().reset_index()
    df['sum'] =np.repeat(df.groupby(['boro'])['count'].sum().values, 5)
    df['percentage'] = df['count'] / df['sum'] * 100

    boros = df.groupby(['boro'])[['count']].sum().sort_values(['count'], ascending=False).index

    fig = px.bar(df, 
                 y='boro', 
                 x='count', 
                 color='grade', 
                 text='percentage',
                 orientation='h',
                 category_orders={'boro': boros,
                                  'grade': ['A', 'B', 'C', 'P', 'NA']})
    
    fig.update_traces(texttemplate='%{text:.1f}%', 
                      textposition='inside',
                      hovertemplate = 'Borough: %{y}' + '<br>Number: %{x}<br>' + 'Percentage: %{text:.1f}%',)
    
    fig.update_layout(title_text='Restaurant grade distribution in different boroughs',
                      xaxis_title="Number of restaurants",
                      yaxis_title="Borough",
                      legend_title='Grade')

    return fig


def plot_grades_cuisine(data, title='', types=False):
    """
    Returns a bar graph of grades based on cuisine.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample. 
    title: string (default: '')
        part of the plot title indicates borough.
    types: bool (default: False)
        plot all cuisine types if False, 
        plot selected cuisines if True. 
    
    Returns:
    --------
    plotly figure
        a bar graph of grades based on cuisine.
    """
    df = data.groupby(['cuisine description', 'grade'])[['count']].sum().reset_index()
    sum_df = df.groupby(['cuisine description'])[['count']].sum().sort_values(['count'], ascending=False).reset_index()
      
    if not types:
        sum_df = sum_df.iloc[:20]
        height = 800
        title = 'Restaurant grade distribution of the top 20 most common cuisine types ' + title
    else:
        height = max(300, 60 * sum_df.shape[0])

        title = 'Restaurant grades distribution ' + title
        
    sum_df.columns = ['cuisine description', 'sum']
    df = pd.merge(sum_df, df, how="left", on='cuisine description')
    df['percentage'] = df['count'] / df['sum'] * 100

    fig = px.bar(df, 
                 y='cuisine description', 
                 x='count', 
                 color='grade', 
                 text='percentage',
                 orientation='h', 
                 height=height,
                 category_orders={'cuisine description': sum_df['cuisine description'],
                                  'grade': ['A', 'B', 'C', 'P', 'NA']})
    fig.update_traces(texttemplate='%{text:.1f}%', 
                      textposition='inside',
                      hovertemplate = 'Cuisine description: %{y}' + '<br>Number: %{x}<br>' + 'Percentage: %{text:.1f}%',)
    fig.update_layout(title_text=title,
                      xaxis_title="Number of restaurants",
                      yaxis_title="Cuisine type",
                      legend_title='Grade')

    return fig


def plot_restaurants(data):
    """
    Returns a plot of grades of selected restaurants over time.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample.
           
    Returns:
    --------
    plotly figure
        a plot of grades of selected restaurants over time
    """
    fig = px.line(data,
                  y='grade', 
                  x='inspection date',
                  color='dba',
                  hover_name="dba", 
                  hover_data=['boro', 'grade', 'inspection date', 'violation description'],
                  category_orders={'grade': ['A', 'P', 'B', 'C', 'NA']},
                  height=500)

    fig.update_traces(mode='markers+lines', 
                      opacity=0.5)

    fig.update_layout(title_text='Restaurant inspection results over time',
                      xaxis_title="Inspection date",
                      yaxis_title="Grade",
                      legend_title='Name')
    
    return fig