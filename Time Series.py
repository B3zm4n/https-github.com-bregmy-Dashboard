import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import subprocess

# Load dataset
data = pd.read_csv('Major_Safety_Events.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Time Series Chart Template"),
    
    # Dropdown for selecting years to display
    dcc.Dropdown(
        id='year-filter',
        options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
        multi=True,
        value=[data['Year'].min()]  # Default selected years
    ),
    
    # Chart to display data
    dcc.Graph(id='time-series-chart')
])

@app.callback(
    Output('time-series-chart', 'figure'),
    Input('year-filter', 'value')
)
def update_chart(selected_years):
    if not selected_years:
        return {}

    filtered_data = data[data['Year'].isin(selected_years)]
    fig = px.line(
        filtered_data,
        x='Event Date',
        y='Total Fatalities',
        title='Total Fatalities Over Time'
    )
    
    return fig

if __name__ == '__main__':
    # Start ngrok to create a public tunnel
    ngrok_process = subprocess.Popen(['ngrok', 'http', '8050'])
    
    app.run_server(debug=True, port='8050')
