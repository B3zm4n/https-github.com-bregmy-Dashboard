import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.graph_objs as go


data = pd.read_csv('Major_Safety_Events.csv')

app = dash.Dash(__name__)

# Define custom CSS styles
app.layout = html.Div(
    style={'background-image': 'url("background.jpg")', 'background-size': 'cover', 'height': '100vh'},
    children=[
        html.Div([
            html.H1("Safety Events Dashboard",
                    style={'text-align': 'center', 'font-size': '36px', 'color': '#007BFF', 'font-family': 'Arial, sans-serif'}),


            # Dropdown for selecting data to visualize
            dcc.Dropdown(
                id='data-selector',
                options=[
                    {'label': col, 'value': col} for col in [
                        "Transit Vehicle Rider Fatalities",
                        "People Waiting or Leaving Fatalities",
                        "Transit Vehicle Operator Fatalities",
                        "Transit Employee Fatalities",
                        "Other Worker Fatalities",
                        "Bicyclist Fatalities",
                        "Pedestrian in Crosswalk Fatalities",
                        "Pedestrian Not in Crosswalk Fatalities",
                        "Pedestrian Crossing Tracks Fatalities",
                        "Pedestrian Walking Along Tracks Fatalities",
                        "Occupant of Other Vehicle Fatalities",
                        "Other Fatalities",
                        "Suicide Fatalities",
                        "Transit Vehicle Rider Injuries",
                        "Transit Vehicle Rider Serious Injuries",
                        "People Waiting or Leaving Injuries",
                        "People Waiting or Leaving Serious Injuries",
                        "Transit Vehicle Operator Injuries",
                        "Transit Vehicle Operator Serious Injuries",
                        "Transit Employee Injuries",
                        "Transit Employee Serious Injuries",
                        "Other Worker Injuries",
                        "Other Worker Serious Injuries",
                        "Bicyclist Injuries",
                        "Bicyclist Serious Injuries",
                        "Pedestrian in Crosswalk Injuries",
                        "Pedestrian in Crosswalk Serious Injuries",
                        "Pedestrian Not in Crosswalk Injuries",
                        "Pedestrian Not in Crosswalk Serious Injuries",
                        "Pedestrian Crossing Tracks Injuries",
                        "Pedestrian Crossing Tracks Serious Injuries",
                        "Pedestrian Walking Along Tracks Injuries",
                        "Pedestrian Walking Along Tracks Serious Injuries",
                        "Occupant of Other Vehicle Injuries",
                        "Occupant of Other Vehicle Serious Injuries",
                        "Other Injuries",
                        "Other Serious Injuries",
                        "Suicide Injuries",
                        "Suicide Serious Injuries",
                        "Total Serious Injuries",
                    ]
                ],
                value="Transit Vehicle Rider Fatalities",  # Default value
                style={'width': '80%', 'margin': '0 auto'},
            ),
        ], style={'background-color': '#f2f2f2', 'padding': '20px'}),

        html.Div([
            # Chart to display data
            dcc.Graph(id='time-series-chart', style={'height': '40vh'}),  # Adjust the chart's height here
        ], style={'width': '80%', 'margin': '0 auto'}),
        
        html.Div([
            html.Div([
                # Heatmap to display data
                dcc.Graph(id='heatmap-chart', style={'height': '40vh'}),  # Adjust the chart's height here
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                # Table to display total fatalities per year
                dash_table.DataTable(
                    id='fatality-table',
                    columns=[{'name': 'Year', 'id': 'Year'}, {'name': 'Total Fatalities', 'id': 'Total Fatalities'}],
                    style_table={'height': '40vh', 'overflowY': 'auto'},  # Adjust the table's height here
                    style_data={'whiteSpace': 'normal', 'height': 'auto'},
                    style_cell={'textAlign': 'left'},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ], style={'width': '80%', 'margin': '0 auto', 'display': 'flex', 'flex-direction': 'row'}),
    ]
)


@app.callback(
    [Output('time-series-chart', 'figure'),
     Output('heatmap-chart', 'figure'),  # Output for heatmap chart
     Output('fatality-table', 'data')],
    Input('data-selector', 'value')
)
def update_chart(selected_data):
    line_chart = go.Figure()
    heatmap_chart = go.Figure()  # Initialize the heatmap chart
    table_data = None
    
    if selected_data:
        # Group data by month and calculate a simple rolling average for the selected column
        data['Event Date'] = pd.to_datetime(data['Event Date'])
        monthly_data = data.set_index('Event Date').groupby(pd.Grouper(freq='M'))[selected_data].sum()
        rolling_avg = monthly_data.rolling(window=3).mean()
        
        # Create a line chart
        line_chart.add_trace(go.Scatter(x=monthly_data.index, y=rolling_avg, mode='lines+markers', name=selected_data))
        line_chart.update_layout(
            title=f'Trends for {selected_data}',
            xaxis_title='Month',
            yaxis_title=selected_data,
            showlegend=True,
            template="plotly",
        )

        # Create a heatmap
        data['Year'] = data['Event Date'].dt.year
        heatmap_data = data.pivot_table(index='Year', columns=data['Event Date'].dt.month, values=selected_data, aggfunc='sum')
        heatmap_chart = go.Figure(data=go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index, colorscale='Viridis'))
        heatmap_chart.update_layout(
            title=f'Heatmap for {selected_data}',
            xaxis_title='Month',
            yaxis_title='Year',
            template="plotly",
        )

        # Create a table showing total fatalities per year
        yearly_fatalities = data.groupby(data['Event Date'].dt.year)[selected_data].sum().reset_index()
        yearly_fatalities.columns = ['Year', 'Total Fatalities']
        table_data = yearly_fatalities.to_dict('records')
    
    return line_chart, heatmap_chart, table_data

if __name__ == '__main__':
    app.run_server(debug=True, port='8050')

