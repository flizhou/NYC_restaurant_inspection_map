
import pandas as pd
import numpy as np
import plotly.express as px


def plot_map(data):

    token = 'pk.eyJ1IjoiZmxpemhvdSIsImEiOiJjazg4Y2hjaW4wMjFlM3NtemhhNG90Z2ZzIn0.gxDbD64mpZbxE2HMjxEZng'

    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", 
                            hover_name="dba", hover_data=["dba"],
                            color_discrete_sequence=["fuchsia"],
                            center=dict(lat=40.7, lon=-74), zoom=10, height=500)
    fig.update_layout(mapbox_accesstoken=token,
                    margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig
    
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
    df = data.groupby(['boro', 'grade'])[['count']].sum().drop(index=['0']).reset_index()
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
    
    fig.update_layout(title_text='The distribution of restaurant grades in differnt boroughs',
                      xaxis_title="Number of restaurants",
                      yaxis_title="Borough",
                      legend_title='Grade')

    return fig


def plot_grades_cuisine(data, code_to_cuisine, title='', types=False):
    """
    Returns a bar graph of grades based on cuisine.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample. 
    code_to_cuisine: dict
        the dict to translate code to cuisine type. 
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
    df = data.groupby(['cuisine type', 'grade'])[['count']].sum().reset_index()
    sum_df = df.groupby(['cuisine type'])[['count']].sum().sort_values(['count'], ascending=False).reset_index()
    
    if not types:
        sum_df = sum_df.iloc[:20]
        title = 'Restaurant grades distribution of top 20 most common cuisine types ' + title
    else:
        title = 'Restaurant grades distribution ' + title
        
    sum_df.columns = ['cuisine type', 'sum']
    sum_df['cuisine description'] = sum_df['cuisine type'].apply(lambda x: code_to_cuisine[str(x)]).values
    df = pd.merge(sum_df, df, how="left", on='cuisine type')
    df['percentage'] = df['count'] / df['sum'] * 100

    fig = px.bar(df, 
                 y='cuisine description', 
                 x='count', 
                 color='grade', 
                 text='percentage',
                 orientation='h', 
                 height=max(200, 40 * sum_df.shape[0]),
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


def plot_restaurants(data, code_to_violation):
    """
    Returns a plot of grades of selected restaurants over time.
    
    Parameters:
    -----------
    data: pandas.DataFrame
        the array of the sample.  
    code_to_violation: dict
        the dict to translation code to violation type.
            
    Returns:
    --------
    plotly figure
        a plot of grades of selected restaurants over time
    """
    data['violation description'] = data['violation type'].apply(lambda x: code_to_violation[str(x)]).values
    fig = px.line(data,
                  y='grade', 
                  x='inspection date',
                  color='camis',
                  hover_name="dba", 
                  hover_data=['camis', 'grade', 'inspection date', 'violation description'],
                  category_orders={'grade': ['A', 'P', 'B', 'C', 'NA']},
                  height=500)

    fig.update_traces(mode='markers+lines', 
                      opacity=0.5)

    fig.update_layout(title_text='Restaurants inspection results over time',
                      xaxis_title="Inspection date",
                      yaxis_title="Grade",
                      legend_title='CAMIS')
    
    return fig