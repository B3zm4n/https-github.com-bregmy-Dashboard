import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from pyngrok import ngrok

# Load dataset 
data = pd.read_csv('Major_Safety_Events.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Tabular Data Template"),
    
    # Dropdown for selecting columns to display
    dcc.Dropdown(
        id='column-filter',
        options=[{'label': col, 'value': col} for col in data.columns],
        multi=True,
        value=data.columns[:5]  # Default selected columns
    ),
    
    # Table to display data
    dash_table.DataTable(
        id='table',
        columns=[{"name": col, "id": col} for col in data.columns],
        data=data.to_dict('records'),
    )
])

@app.callback(
    dash.dependencies.Output('table', 'columns'),
    dash.dependencies.Output('table', 'data'),
    dash.dependencies.Input('column-filter', 'value')
)
def update_table(selected_columns):
    if not selected_columns:
        return [], []

    updated_columns = [{"name": col, "id": col} for col in selected_columns]
    updated_data = data[selected_columns].to_dict('records')
    
    return updated_columns, updated_data

if __name__ == '__main__':
    app.run_server(debug=True, port='8050')  # Use a specific port for ngrok

    # Create a public ngrok tunnel to the Dash app
    public_url = ngrok.connect(port='8050')
    print(" * ngrok tunnel \"{}\" -> http://127.0.0.1:8050".format(public_url))
