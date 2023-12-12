import dash
import json
import plotly.express as px
from dash import dcc, html
import pandas as pd

# Load the data
df = pd.read_csv("pollution_data.csv")

# Convert 'Date Local' column to datetime
df['Date Local'] = pd.to_datetime(df['Date Local'])

# Extract year from the 'Date Local' column
df['Year'] = df['Date Local'].dt.year

# Create a Dash web application
app = dash.Dash(__name__)

with open("us-states.json", "r") as geojson_file:
    us_states_geojson = json.load(geojson_file)

us_map = dcc.Graph(
    id='us-pollution-map',
    className='graph-container',
    style={'width': '25%', 'height': '500px'},
    figure=px.choropleth_mapbox(
        df,
        geojson=us_states_geojson,
        locations='State',
        featureidkey="properties.name",
        color='NO2 Mean',  # Change to the desired pollution variable
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3,
        opacity=0.5,
        labels={'NO2 Mean': 'NO2 Mean'}  # Change label as needed
    ),
    clickData=None  # Initialize clickData to None
)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Pollution Statistics Dashboard"),

    html.Div([
        dcc.Graph(id='no2-graph', className='graph-container', style={'width': '25%'}),
        dcc.Graph(id='o3-graph', className='graph-container', style={'width': '25%'}),
        dcc.Graph(id='so2-graph', className='graph-container', style={'width': '25%'}),
        dcc.Graph(id='co-graph', className='graph-container', style={'width': '25%'}),
    ], className='row', style={'display': 'flex'}),

    # Add a map at the bottom
    html.Div([
        dcc.Graph(id='bar-line-graph', className='graph-container', style={'width': '25%', 'height': '500px'}),
        us_map,
        dcc.Graph(id='pie-chart', className='graph-container', style={'width': '25%', 'height': '500px'}),
        dcc.Markdown('''
                        ### Pollution Types and Effects

                        - **NO2 (Nitrogen Dioxide):**
                          - Effects: Irritates the respiratory system, can lead to respiratory infections.

                        - **O3 (Ozone):**
                          - Effects: Causes respiratory problems, aggravates asthma, and reduces lung function.

                        - **SO2 (Sulfur Dioxide):**
                          - Effects: Irritates the respiratory system, can worsen asthma, and contributes to acid rain.

                        - **CO (Carbon Monoxide):**
                          - Effects: Reduces the blood's ability to carry oxygen, leading to headaches and dizziness.
                    ''', style={'width': '25%', 'height': '500px'}),
    ], className='row', style={'display': 'flex'}),
])


# Define callback to update graphs and map based on map click
@app.callback(
    [dash.dependencies.Output('no2-graph', 'figure'),
     dash.dependencies.Output('o3-graph', 'figure'),
     dash.dependencies.Output('so2-graph', 'figure'),
     dash.dependencies.Output('co-graph', 'figure'),
     dash.dependencies.Output('bar-line-graph', 'figure'),
     dash.dependencies.Output('pie-chart', 'figure')],
    [dash.dependencies.Input('us-pollution-map', 'clickData')]
)
def update_graphs_and_map(clickData):
    if clickData:
        selected_state = clickData['points'][0]['location']
        filtered_df = df[df['State'] == selected_state]

        pollution_info = f"**{selected_state} Pollution Levels:**\n" \
                         f"- NO2 Mean: {filtered_df['NO2 Mean'].mean():.2f}\n" \
                         f"- O3 Mean: {filtered_df['O3 Mean'].mean():.2f}\n" \
                         f"- SO2 Mean: {filtered_df['SO2 Mean'].mean():.2f}\n" \
                         f"- CO Mean: {filtered_df['CO Mean'].mean():.2f}"

        # Group data by year and calculate the mean for each year
        yearly_df = filtered_df.groupby('Year').mean().reset_index()

        # Common layout settings for all graphs
        common_layout = {
            'title': 'Pollution',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Mean Value'},
            'mode': 'lines+markers',
        }

        # Smaller graph height
        smaller_height = 300

        # NO2 Graph
        no2_graph = {
            'data': [
                {'x': yearly_df['Year'], 'y': yearly_df['NO2 Mean'], 'type': 'scatter', 'name': 'NO2 Mean'},
                # Add other NO2 related data here if needed
            ],
            'layout': {**common_layout, 'height': smaller_height, 'title': 'NO2 Pollution'}
        }

        # O3 Graph
        o3_graph = {
            'data': [
                {'x': yearly_df['Year'], 'y': yearly_df['O3 Mean'], 'type': 'scatter', 'name': 'O3 Mean'},
                # Add other O3 related data here if needed
            ],
            'layout': {**common_layout, 'height': smaller_height, 'title': 'O3 Pollution'}
        }

        # SO2 Graph
        so2_graph = {
            'data': [
                {'x': yearly_df['Year'], 'y': yearly_df['SO2 Mean'], 'type': 'scatter', 'name': 'SO2 Mean'},
                # Add other SO2 related data here if needed
            ],
            'layout': {**common_layout, 'height': smaller_height, 'title': 'SO2 Pollution'}
        }

        # CO Graph
        co_graph = {
            'data': [
                {'x': yearly_df['Year'], 'y': yearly_df['CO Mean'], 'type': 'scatter', 'name': 'CO Mean'},
                # Add other CO related data here if needed
            ],
            'layout': {**common_layout, 'height': smaller_height, 'title': 'CO2 Pollution'}
        }

        bar_line_graph = {
            'data': [
                {'x': yearly_df['Year'], 'y': yearly_df['NO2 Mean'], 'type': 'bar', 'name': 'NO2 Mean'},
                {'x': yearly_df['Year'], 'y': yearly_df['O3 Mean'], 'type': 'scatter', 'name': 'O3 Mean',
                 'yaxis': 'y2'},
            ],
            'layout': {
                'title': f'{selected_state} Bar-Line Graph',
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'NO2 Mean'},
                'yaxis2': {'title': 'O3 Mean', 'overlaying': 'y', 'side': 'right'},
            },
        }

        # Pie chart
        pie_chart = {
            'data': [
                {'labels': ['NO2', 'O3', 'SO2', 'CO'],
                 'values': [filtered_df['NO2 Mean'].mean(), filtered_df['O3 Mean'].mean(),
                            filtered_df['SO2 Mean'].mean(), filtered_df['CO Mean'].mean()],
                 'type': 'pie',
                 'marker': {'colors': ['red', 'green', 'blue', 'orange']},
                 'textinfo': 'label+percent',
                 'hole': 0.3}
            ],
            'layout': {
                'title': f'{selected_state} Pollution Distribution',
            }
        }

        return no2_graph, o3_graph, so2_graph, co_graph, bar_line_graph, pie_chart

    # If no clickData, return empty figures
    return px.scatter(), px.scatter(), px.scatter(), px.scatter(), px.scatter(), px.pie()


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)
